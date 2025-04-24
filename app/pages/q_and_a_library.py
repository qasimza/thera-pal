import streamlit as st
import pandas as pd
import os
from streamlit_tags import st_tags
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cache the data load so it isn't read again on every rerun.
@st.cache_data
def load_data(data_path):
    return pd.read_csv(data_path)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "thera_pal_dataset.csv")
df_original = load_data(DATA_PATH)

st.title("TheraPal Q&A Library")
st.markdown(
    "Browse a growing database of real questions answered by professional counselors. "
    "Learn from peer experiences and deepen your therapeutic toolkit with insights grounded in practice."
)

# Tag-style input for keywords.
keywords = st_tags(
    label='Enter keywords:',
    text='Press enter to add more',
    value=[],  # Start with empty list.
    suggestions=[],
    maxtags=10,
    key='1'
)

# Other filters.
topics = st.multiselect("Filter by topic", options=sorted(df_original['topic'].dropna().unique()))
advice_filters = st.multiselect("Filter by advice type", options=sorted(df_original['adviceType'].dropna().unique()))

# Function: Create a combined text column on a copy of the dataframe.
def add_combined_text(df):
    df_copy = df.copy()
    df_copy['combined_text'] = (
        df_copy['questionTitle'].fillna('') + ' ' +
        df_copy['questionText'].fillna('') + ' ' +
        df_copy['answerText'].fillna('') + ' ' +
        df_copy['topic'].fillna('') + ' ' +
        df_copy['adviceType'].fillna('')
    )
    return df_copy

# Cached function to compute the TF-IDF vectorizer and matrix.
@st.cache_data
def compute_tfidf(df, combined_text_col='combined_text'):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df[combined_text_col])
    return vectorizer, tfidf_matrix

# Function: Get a filtered DataFrame based on keywords using TF-IDF similarity.
def filter_by_keywords(df, keywords):
    if not keywords:
        return df
    query = " ".join(keywords).lower()
    # Ensure we have a combined text column.
    df_with_text = add_combined_text(df)
    vectorizer, tfidf_matrix = compute_tfidf(df_with_text)
    query_vec = vectorizer.transform([query])
    # Calculate cosine similarities.
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    df_with_text['similarity'] = similarities
    # Filter out rows with no similarity.
    return df_with_text[df_with_text['similarity'] > 0].sort_values(by='similarity', ascending=False)

# Start with the original DataFrame (we do not modify df_original).
filtered_df = df_original.copy()

# First, apply keyword filtering.
if keywords:
    filtered_df = filter_by_keywords(filtered_df, keywords)
else:
    # Also add combined_text for consistency with later operations.
    filtered_df = add_combined_text(filtered_df)

# Then, apply topic and advice type filters.
if topics:
    filtered_df = filtered_df[filtered_df['topic'].isin(topics)]
if advice_filters:
    filtered_df = filtered_df[filtered_df['adviceType'].isin(advice_filters)]

# Display Results.
st.markdown("### Search Results")
if not keywords and not topics and not advice_filters:
    st.markdown("_Try adding keywords or using filters to see more specific results._")

if not filtered_df.empty:
    # Group for question metadata (excluding therapist details, which are answer-specific).
    question_metadata = (
        filtered_df
        .groupby('questionID')
        .agg({
            'questionTitle': 'first',
            'questionText': 'first',
            'topic': lambda x: ', '.join(sorted({str(val) for val in x if pd.notnull(val)})),
            'questionLink': 'first',
            'upvotes': 'first',
            'views': 'first'
        })
        .reset_index()
    )

    # Group answers including therapist details so that each unique answer by a specific therapist is preserved.
    grouped_answers = (
        filtered_df
        .groupby(['questionID', 'answerText', 'therapistInfo', 'therapistURL'])
        .agg({
            'adviceType': lambda x: ', '.join(sorted({str(val) for val in x if pd.notnull(val)}))
        })
        .reset_index()
    )

    # Iterate over each question and render the metadata.
    for _, question in question_metadata.iterrows():
        st.markdown(f"#### {question['questionTitle']}")
        st.markdown(question['questionText'])
        st.markdown(f"**Topics:** {question['topic']}")
        st.markdown(f"[🔗 View Full Question]({question['questionLink']})")
        st.markdown(f"👍 **Upvotes:** {question['upvotes']} &nbsp;&nbsp; 👁️ **Views:** {question['views']}")

        # Filter the answers to this question.
        answers = grouped_answers[grouped_answers['questionID'] == question['questionID']]
        for _, answer in answers.iterrows():
            st.markdown(f"##### Answer ({answer['adviceType']}):")
            st.markdown(answer['answerText'])
            st.markdown(
                f"👤 **Therapist:** [{answer['therapistInfo']}]({answer['therapistURL']})"
            )
            st.markdown("---")
else:
    if keywords or topics or advice_filters:
        st.markdown("No results found. Try refining your search or filter criteria.")
