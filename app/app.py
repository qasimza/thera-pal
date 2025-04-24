import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


st.write("# Welcome to TheraPal! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    __Your trusted companion in therapeutic guidance—powered by insights from over 300 professionals.__
    TheraPal draws on a rich dataset of `804` unique questions answered by `307` therapists, with over `2,100` responses spanning `31` topics. Each question has been answered __at least once__, with an average of `2.61` responses per question—ensuring diverse, well-rounded perspectives to support your practice.
    
    ### 1. 💬 AI-Powered Assistant  
    Ask questions and receive instant, research-informed guidance on how to approach patient concerns. Our GPT-powered assistant is trained on expert resources to help you find the right words, strategies, and support—when you need it most.  
    Currently, we support 4 advice types:
    - 🛠️ __Practical Life Advice__: Actionable suggestions to improve sleep, routine, self-care, gratitude, or navigating social environments.  
    - 💖 __Emotional Support and Validation__: Empathetic, validating responses that help users feel understood and emotionally safe.  
    - 📚 __Resource Suggestion__: Directing users to professional help, helplines, books, online resources, or specific therapies like CBT or ACT.  
    - 🧠 __Psychoeducation__: Clear explanations of mental health symptoms, conditions, therapy processes, or psychological mechanisms.

   
    #### Disclaimer 
    __TheraPal is an experimental tool designed to support therapists by generating suggestions based on a dataset of real counselor responses and large language models. The information provided is not medical advice, and is not a substitute for professional training, clinical judgment, or direct consultation with a licensed mental health professional.__  

    While the assistant has been trained on publicly available therapeutic Q&A and guided by best practices in mental health support, its recommendations may not be appropriate for every situation or client. Always evaluate AI-generated guidance within the context of individual patient needs and consult appropriate professionals when necessary.  
   
    ### 2. 📚 Therapist Q&A Library  
    Browse a growing database of real questions answered by professional counselors. Learn from peer experiences and deepen your therapeutic toolkit with insights grounded in practice.  
"""
)