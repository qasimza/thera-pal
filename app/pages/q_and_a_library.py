import streamlit as st
import pandas as pd
import os
from streamlit_tags import st_tags
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@st.cache_data
def load_data(data_path):
    df = pd.read_csv(data_path)
    df['combined_text'] = (
            df['questionTitle'].fillna('') + ' ' +
            df['questionText'].fillna('') + ' ' +
            df['answerText'].fillna('') + ' ' +
            df['topic'].fillna('') + ' ' +
            df['adviceType'].fillna('')
    )
    return df


@st.cache_data
def compute_vectorizer(df):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(df['combined_text'])
    return vectorizer, tfidf_matrix


def rank_data(df, keywords, selected_topics, selected_advice):
    df = df.copy()

    # Compute TF-IDF similarity if keywords are provided
    if keywords:
        vectorizer, tfidf_matrix = compute_vectorizer(df)
        query_vec = vectorizer.transform([" ".join(keywords)])
        df['similarity'] = cosine_similarity(query_vec, tfidf_matrix).flatten()
    else:
        df['similarity'] = 0

    # Combine all selected filters
    total_filters = len(selected_topics) + len(selected_advice)

    def combined_match_count(row):
        count = 0
        if selected_topics and row['topic'] in selected_topics:
            count += 1
        if selected_advice and row['adviceType'] in selected_advice:
            count += 1
        return count

    if total_filters > 0:
        df['match_pct'] = df.apply(lambda row: 100 * combined_match_count(row) / total_filters, axis=1)
    else:
        df['match_pct'] = 0

    # Filter: keep only rows with matches

    if keywords and (selected_topics or selected_advice):
        df = df[(df['similarity'] > 0) & (df['match_pct'] > 0)]
        df = df.sort_values(by=['match_pct', 'similarity'], ascending=[False, False])
    elif keywords:
        df = df[(df['similarity'] > 0)]
        df = df.sort_values(by='similarity', ascending=False)
    elif selected_topics or selected_advice:
        df = df[(df['match_pct'] > 0)]
        df = df.sort_values(by='match_pct', ascending=False)

    return df


# File path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "thera_pal_dataset.csv")
df_original = load_data(DATA_PATH)

# UI
st.title("TheraPal Q&A Library")
st.markdown(
    "Browse a growing database of real questions answered by professional counselors. "
    "Learn from peer experiences and deepen your therapeutic toolkit with insights grounded in practice."
)

keywords = st_tags(
    label='Enter keywords, phrases or questions (max=10):',
    text='Press enter to add more',
    value=[],
    suggestions=[],
    maxtags=10,
    key='1'
)

topics = st.multiselect("Filter by topic", options=sorted(df_original['topic'].dropna().unique()))
advice_types = st.multiselect("Filter by advice type", options=sorted(df_original['adviceType'].dropna().unique()))

# Filtering
ranked_df = rank_data(df_original, keywords, topics, advice_types)

st.markdown("### Search Results")

# Display
if not keywords and not topics and not advice_types or ranked_df.empty:
    st.markdown("_Try adding or modifying the keywords/filters to see more results._")

elif not ranked_df.empty:

    grouped_questions = ranked_df.groupby(['questionID', 'questionTitle', 'questionText', 'questionLink', 'topic'])

    for (qid, title, qtext, qlink, topic), group in grouped_questions:
        st.markdown(f"### {title}")
        st.markdown(qtext)
        st.markdown(f"**Topics:** {topic}")
        st.markdown(f"[🔗 View Full Question]({qlink})")

        # Group answers uniquely by answerText to deduplicate
        answer_groups = group.groupby('answerText')

        for answer_text, ans_group in answer_groups:
            advice_types = list({t for t in ans_group['adviceType'].dropna()})
            row = ans_group.iloc[0]  # One therapist, upvotes, etc. per answer

            st.markdown(f"**Answer ({', '.join(advice_types)}):**")
            st.markdown(f"👍 **Upvotes:** {row['upvotes']} &nbsp;&nbsp; 👁️ **Views:** {row['views']}")
            st.markdown(answer_text)
            st.markdown(f"👤 [{row['therapistInfo']}]({row['therapistURL']})")
            st.markdown("")

        st.markdown("---")

else:
    st.warning("No results found. Try refining your search or filter criteria.")
