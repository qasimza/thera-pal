import pickle
import os
import streamlit as st

# Set the page config (optional)
st.set_page_config(page_title="Therapist Advice Classifier", layout="centered")

# Load the model
@st.cache_resource
def load_model(model_path):
    with open(model_path, 'rb') as file:
        return pickle.load(file)

# Prediction function
def get_prediction(document, model):
    prediction = model.predict([document])
    labels = ['Practical Life Advice', 'Emotional Support and Validation', 'Resource Suggestion', 'Psychoeducation']
    result = [label for value, label in zip(prediction[0], labels) if value]
    return result

# Load the model
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, "classifier", "therapal_classifier.sav")
model = load_model(MODEL_PATH)

st.title("Therapist Advice Type Classifier")

user_input = st.text_area("Enter a therapist's answer:", height=200)

if st.button("Classify"):
    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        prediction = get_prediction(user_input, model)
        if prediction:
            st.success("Classified Advice Types:")
            for label in prediction:
                st.markdown(f"- ✅ **{label}**")
        else:
            st.info("No advice type identified.")
