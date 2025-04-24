# TheraPal

## Overview
A modern companion for therapists and counsellors to use when they need guidance on how to best help a patient. 

This application is a preliminary version, a "proof of concept," demonstrating the core idea or functionality. It's not intended for full-scale production use, as the production version will be significantly different in terms of features, robustness, and scaling.

## How to run the app locally
1. Clone the repo
```
git clone https://github.com/qasimza/thera-pal.git
```
2. Install the requirements
```
pip install -r requirements.txt
```
3. Create a `.streamlit/secrets.toml` file in the root directory and add the OPEN_API_KEY to it.
```
touch .streamlit/secrets.toml
OPEN_API_KEY='insert_your_key'
```
5. Run the app
```
streamlit run app/app.py 
```

## References
[Streamlit](https://docs.streamlit.io/)
