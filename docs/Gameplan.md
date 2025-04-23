# TheraPal

## High-Level Strategy
__Time Limit__: 4 hours (5 maximum)

__Focus__: Fastest path to a working, demoable product which meets all the requirements.

__Tech Stack Considerations__: Lean, fast-to-deploy, and familiar.

__Goal__: Give mental health counselors a helpful assistant via a web app that combines data-backed insights and LLM-generated advice.

__Bonus__: Give a little something extra! 

## Chosen Direction
I'll go with Option 3 for the web app:  
>__"Users can enter free-text describing a challenge with a patient, and get LLM-generated suggestions on how to help."__

This has the most immediate "magic" for a demo and feels like a product prototype investors or users could fall in love with.

## Step-by-Step Plan
### Step 1: Dataset (20 min)
Use the CounselChat dataset — counseling Q&A format, perfect for this task. 

Preprocess into a pandas DataFrame. 

For speedy development, I'm initially storing the dataset in memory. With approximately 4,000 rows, I believe this approach won't significantly impact application performance. However, a production environment would implement a more scalable data storage solution as well as account for new data to be scraped and stored. Derived insights should also be stored. 

### Step 2: Quick Exploratory Data Analysis & Insight (30 min)
Use basic NLP:

TF-IDF vectorization or simple text embeddings (e.g., OpenAI or SentenceTransformers)

Cluster by topic (KMeans or HDBSCAN)

Categorize answers by advice type: Direct advice, empathetic response, resource suggestion, etc. (simple rule-based classifier or use zero-shot classification with LLM)

Choosing one categorical feature: “Type of advice”.

### Step 3: Build ML Model (40 min)
Predict “Advice Type” from user prompt using a classifier.

Preliminary Choice: Zero-shot classification with OpenAI (text-classification prompt to gpt-3.5-turbo).

Alternative: If Zero-shot classification proves to be expensive, in-accurate or inefficient, it may be worth considering other LSTM techniques. 

Keep model simple: LogisticRegression + TF-IDF OR call OpenAI zero-shot with a few examples.

### Step 4: Build LLM Suggestion System (45 min)
Use OpenAI `gpt-3.5-turbo` to:

Generate suggestions for the counselor.

Prompt example:

> A counselor is helping a patient with {user_input}.
Based on prior counseling sessions, suggest an appropriate way to respond.
Keep it professional, empathetic, and evidence-based.

Use 2–3 examples from the dataset as few-shot context.

### Step 5: Build Web App (1 hour)
__Framework__: Streamlit (crazy fast to build interactive apps).

__Three key sections__:

1. __Input Box__: Free text input of user problem.

2. __LLM Output__: Streamed/generated suggestion from GPT.

3. __Advice Type__: Add dropdown to show predicted "Advice Type".

4. __Bonus Sidebar__: Add a sidebar to browse similar Q&A from dataset using sentence similarity.

### Tools & Stack

__Programming Language__: Python  
__Web Application Framework__: Streamlit


### Deliverables (in 4 hours)
- Working Streamlit app
- LLM suggestion feature (core wow)
- Basic classifier for “advice type” (optional but cool)
- (Optional) Search similar questions
- Clean README.md

### Bonus Thoughts

Include a “What not to say” checklist in the LLM prompt.

Add a disclaimer (“This tool is not a substitute for clinical judgment”)

### TL;DR: The MVP in Action
User types: 

>“My patient is struggling with imposter syndrome at work.”

App returns:

>“Acknowledge their accomplishments and validate their feelings. Encourage them to keep a journal of successes, and suggest discussing these thoughts with a CBT specialist.”



