# app/routes.py

from flask import render_template, request, redirect, url_for
from app import app
from app.classifier import train_model, classify_text, generate_predictions
from app.utils import save_file, allowed_file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = save_file(file)
        train_model('uploads/' + filename)
        return redirect(url_for('classify'))
    return redirect(url_for('index'))

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        text = request.form['text']
        if not text:
            return render_template('classify.html', prediction="No text provided")
        try:
            predicted_status = classify_text(text)
            return render_template('classify.html', prediction=predicted_status)
        except ValueError as e:
            return render_template('classify.html', prediction=str(e))
    return render_template('classify.html', prediction=None)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = save_file(file)
            predictions = generate_predictions('uploads/' + filename)
            return render_template('predictions.html', predictions=predictions)
    return render_template('predict.html')

