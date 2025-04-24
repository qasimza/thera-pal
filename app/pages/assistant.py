from openai import OpenAI
import streamlit as st

# Configuration
MODEL = "gpt-4.1-mini"

# Define advice types and their descriptions
ADVICE_TYPES = {
    "Direct advice": "Give clear, actionable steps a therapist can share with the patient.",
    "Empathetic response": "Suggest ways the therapist can validate the patient’s feelings and build rapport.",
    "Resource suggestion": "Recommend tools, exercises, or materials the therapist can offer the patient.",
    "Diagnosis": "Help assess whether the patient's symptoms align with a mental health condition, based on their description.",
    "Treatment": "Suggest therapeutic approaches or medication the therapist could use to support the patient's recovery."
}


st.title("TheraPal Assistant")

# Sidebar for configuring advice type
selected_advice_types = st.multiselect(
    "Select the type(s) of advice you'd like:",
    ADVICE_TYPES.keys(),
    default=["Direct advice"]
)

# Build a dynamic system prompt based on selected advice types
formatted_types = ', '.join([
    advice_type + (':' + ADVICE_TYPES[advice_type] if ADVICE_TYPES[advice_type] else '')
    for advice_type in selected_advice_types
])

dynamic_prompt = f"""
# Identity

You are a mental health assistant providing professional support to therapists.

# Instructions

Please respond to the therapist’s query with the following types of advice: 
{formatted_types}
Tailor your responses accordingly and maintain a professional, supportive tone.
Limit the response to 1500 characters.
"""

# Store the dynamic prompt in session state (not added to chat history)
st.session_state["dynamic_prompt"] = dynamic_prompt

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize session state if needed
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = MODEL

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display user/assistant chat messages (skip system message)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input prompt
user_input = st.chat_input("Describe your patient's situation and what guidance you’re looking for.")

if user_input:
    # Append user's message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "system", "content": st.session_state["dynamic_prompt"]}
            ] + st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)

    # Append assistant's response
    st.session_state.messages.append({"role": "assistant", "content": response})
