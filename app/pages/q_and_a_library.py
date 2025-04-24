import streamlit as st
import pandas as pd
import os

# Load processed data
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "classified_results.csv")
df = pd.read_csv(DATA_PATH)

st.title("TheraPal Q&A Library")
st.markdown("Browse a growing database of real questions answered by professional counselors. Learn from peer experiences and deepen your therapeutic toolkit with insights grounded in practice.")


# Get the absolute path to the project root


# Search input
search_query = st.text_input("Search for a question:")
topics = st.multiselect("Filter by topic", options=sorted(df['topic'].dropna().unique()))
advice_filters = st.multiselect("Filter by advice type", options=sorted(df['adviceType'].dropna().unique()))

# Apply filters
filtered_df = df.copy()

if search_query:
    filtered_df = filtered_df[filtered_df['questionText'].str.contains(search_query, case=False, na=False)]

if topics:
    filtered_df = filtered_df[filtered_df['topic'].isin(topics)]

if advice_filters:
    filtered_df = filtered_df[filtered_df['adviceType'].apply(lambda x: any(typ in x for typ in advice_filters))]

# Display results
for qid, group in filtered_df.groupby("questionID"):
    st.markdown(f"### {group.iloc[0]['questionTitle']}")
    st.markdown(group.iloc[0]['questionText'])

    for idx, row in group.iterrows():
        st.markdown(f"**Answer ({row['classified_advice_types']}):**")
        st.markdown(row['answerText'])
        st.markdown("---")
