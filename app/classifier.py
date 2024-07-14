# classifier.py

import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from app.preprocess import tokenize_normalize  

# Predefined list of animal names
df = pd.read_json("animals.json")
animal_names = df['animals'].tolist()

classifier = None
vectorizer = None
label_map = None

def train_model(data_path):
    global classifier, vectorizer, label_map
    
    data = pd.read_json(data_path)
    texts = data['text'].tolist()
    labels = data['label'].tolist()
    label_map = {label: idx for idx, label in enumerate(set(labels))}
    y = [label_map[label] for label in labels]
    vectorizer = TfidfVectorizer(preprocessor=tokenize_normalize)  
    X = vectorizer.fit_transform(texts)
    classifier = LogisticRegression()
    classifier.fit(X, y)

def classify_text(text):
    global classifier, vectorizer, label_map
    
    if classifier is None or vectorizer is None or label_map is None:
        raise RuntimeError("Model not trained yet. Please upload training data.")
    
    # Preprocessing input text
    processed_text = tokenize_normalize(text)
    
    # Find animal names in the text using regex
    detected_animals = [animal for animal in animal_names if re.search(r'\b{}\b'.format(animal), processed_text, re.IGNORECASE)]
    
    if not detected_animals:
        raise ValueError("No recognized animal names found in the input.")
    
    predictions = []
    for animal in detected_animals:
        vectorized_text = vectorizer.transform([animal])
        prediction = classifier.predict(vectorized_text)
        
        if prediction[0] not in label_map.values():
            predictions.append({"animal": animal, "predicted_status": "Unknown"})
        else:
            status = [k for k, v in label_map.items() if v == prediction[0]][0]
            predictions.append({"animal": animal, "predicted_status": status})
    
    return predictions

def generate_predictions(data_path):
    global classifier, vectorizer, label_map
    data = pd.read_json(data_path)
    texts = data['text'].tolist()
    predictions = []
    for text in texts:
        try:
            predicted_statuses = classify_text(text)
            predictions.extend(predicted_statuses)
        except ValueError as e:
            predictions.append({"text": text, "predicted_label": str(e)})
        except RuntimeError as e:
            predictions.append({"text": text, "predicted_label": str(e)})
    return predictions
