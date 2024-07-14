import pandas as pd
import streamlit as st
from app.classifier import train_model, classify_text
from app.utils import save_file, allowed_file
import os

# Function to display the index page
def index_page():
    st.title("Index Page")
    st.write("Welcome to the Index Page! Use the sidebar to navigate to other pages.")

# Function to display the upload page
def upload_page():
    st.title("Upload Dataset")
    uploaded_file = st.file_uploader("Choose a file", type=['json'])
    if uploaded_file is not None:
        if allowed_file(uploaded_file.name):
            filename = save_file(uploaded_file)
            train_model('uploads/' + filename)
            st.success(f"File {uploaded_file.name} uploaded and model trained successfully!")
        else:
            st.error("File type not allowed.")

# Function to display the classify page
def classify_page():
    st.title("Classify Text Page")
    text_input = st.text_area("Enter text here:", height=150)
    if st.button("Classify"):
        if text_input:
            try:
                predictions = classify_text(text_input)
                df = pd.DataFrame(predictions)
                st.subheader("Predicted Status:")
                st.table(df)
            except ValueError as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter some text for classification.")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Index Page", "Upload Page", "Classify Text Page"])

    if page == "Index Page":
        index_page()
    elif page == "Upload Page":
        upload_page()
    elif page == "Classify Text Page":
        classify_page()
  

if __name__ == "__main__":
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    main()
