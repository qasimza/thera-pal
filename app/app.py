import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Therapal! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    __Your trusted companion in therapeutic guidance—powered by insights from over 300 professionals.__
    TheraPal draws on a rich dataset of `804` unique questions answered by `307` therapists, with over `2,100` responses spanning `31` topics. Each question has been answered __at least once__, with an average of `2.61` responses per question—ensuring diverse, well-rounded perspectives to support your practice.
    
    ### 1. 💬 AI-Powered Assistant  
    Ask questions and receive instant, research-informed guidance on how to approach patient concerns. Our GPT-powered assistant is trained on expert resources to help you find the right words, strategies, and support—when you need it most.  
    
    ### 2. 📚 Therapist Q&A Library  
    Browse a growing database of real questions answered by professional counselors. Learn from peer experiences and deepen your therapeutic toolkit with insights grounded in practice.  
"""
)