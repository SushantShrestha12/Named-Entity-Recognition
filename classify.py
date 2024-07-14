import streamlit as st

# Set the title of the app
st.title("Classify Text")

# Create a text area for user input
text_input = st.text_area("Enter text here:", height=150)

# Create a button for classification
if st.button("Classify"):
    if text_input:
        # Dummy prediction for demonstration purposes
        # Replace this with your actual text classification logic
        prediction = "Positive" if "good" in text_input.lower() else "Negative"
        
        # Display the predicted status
        st.subheader(f"Predicted Status: {prediction}")
    else:
        st.warning("Please enter some text for classification.")
