# preprocess.py

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def tokenize_normalize(text):
    # Tokenization
    words = word_tokenize(text)
    
    # Normalization: Removing stopwords and lemmatization
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word.isalpha() and word.lower() not in stop_words]
    
    # Joining the words back into a single string
    processed_text = ' '.join(words)
    
    return processed_text
