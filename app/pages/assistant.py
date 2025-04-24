from openai import OpenAI
import streamlit as st

# Configuration
MODEL = "gpt-3.5-turbo"
ADVICE_TYPES = {
    "Direct advice":"",
    "Empathetic response":"",
    "Resource suggestion":"",
    "Diagnosis":"",
    "Treatment":""
}

st.title("TheraPal Assistant")

# Sidebar for configuring advice type
selected_advice_types = st.multiselect(
    "Select the type(s) of advice you'd like:",
    ADVICE_TYPES.keys(),
    default=["Direct advice"]
)

# Build a dynamic system prompt based on selected advice types
dynamic_prompt = f"""
# Identity

You are a mental health assistant providing professional support to therapists.

# Instructions

Please respond to the therapist’s query with the following types of advice: 
{', '.join([advice_type+':'+ADVICE_TYPES[advice_type] for advice_type in selected_advice_types])} 
Tailor your responses accordingly and maintain a professional, supportive tone.
Limit the response to 1500 characters.
"""

# OpenAI client
client = OpenAI(api_key=OPEN_AI_KEY)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = MODEL

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": dynamic_prompt}]

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Updated input prompt
user_input = st.chat_input("Describe your patient's situation and what guidance you’re looking for.")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
