import streamlit as st
import pandas as pd
import os
from streamlit_tags import st_tags
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

keywords = st_tags(
    label='Enter keywords:',
    text='Press enter to add more',
    value=[],
    suggestions=[],
    maxtags=10,
    key='1'
)

topics = st.multiselect("Filter by topic", options=sorted(df_original['topic'].dropna().unique()))
advice_filters = st.multiselect("Filter by advice type", options=sorted(df_original['adviceType'].dropna().unique()))

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

@st.cache_data
def compute_tfidf(df, combined_text_col='combined_text'):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df[combined_text_col])
    return vectorizer, tfidf_matrix

def filter_by_keywords_and_tags(df, keywords, selected_topics, selected_advice):
    df = add_combined_text(df)

    # TF-IDF similarity score
    if keywords:
        query = " ".join(keywords).lower()
        vectorizer, tfidf_matrix = compute_tfidf(df)
        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    else:
        similarities = [0] * len(df)

    df['similarity'] = similarities

    # Aggregate topics and adviceTypes per question-answer combo
    df_grouped = (
        df.groupby(['questionID', 'answerText', 'therapistInfo', 'therapistURL', 'questionTitle', 'questionText', 'questionLink', 'upvotes', 'views'])
        .agg({
            'topic': lambda x: list({t.strip() for t in x.dropna()}),
            'adviceType': lambda x: list({a.strip() for a in x.dropna()}),
            'similarity': 'max'
        })
        .reset_index()
    )

    # Compute match counts
    def match_count(row, selected, field):
        return sum(1 for item in row[field] if item in selected) if selected else 0

    df_grouped['topic_match_count'] = df_grouped.apply(lambda row: match_count(row, selected_topics, 'topic'), axis=1)
    df_grouped['advice_match_count'] = df_grouped.apply(lambda row: match_count(row, selected_advice, 'adviceType'), axis=1)

    # Final ranking score
    df_grouped['total_score'] = df_grouped['similarity'] + 0.1 * (df_grouped['topic_match_count'] + df_grouped['advice_match_count'])
    df_grouped = df_grouped.sort_values(by='total_score', ascending=False)

    return df_grouped

# Apply all filters
filtered_df = filter_by_keywords_and_tags(df_original, keywords, topics, advice_filters)

# Display results
if not keywords and not topics and not advice_filters:
    st.markdown("### Sample Results")
    st.markdown("_Try adding keywords or using filters to see more specific results._")

elif not filtered_df.empty:
    st.markdown("### Search Results")

    for _, row in filtered_df.iterrows():
        st.markdown(f"#### {row['questionTitle']}")
        st.markdown(row['questionText'])
        st.markdown(f"**Topics:** {', '.join(row['topic'])}")
        st.markdown(f"[🔗 View Full Question]({row['questionLink']})")
        st.markdown(f"👍 **Upvotes:** {row['upvotes']} &nbsp;&nbsp; 👁️ **Views:** {row['views']}")
        st.markdown(f"##### Answer ({', '.join(row['adviceType'])}):")
        st.markdown(row['answerText'])
        st.markdown(
            f"👤 **Therapist:** [{row['therapistInfo']}]({row['therapistURL']})"
        )
        st.markdown("---")

else:
    st.markdown("No results found. Try refining your search or filter criteria.")
