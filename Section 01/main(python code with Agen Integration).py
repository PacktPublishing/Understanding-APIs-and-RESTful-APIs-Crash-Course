import streamlit as st
from google_play_scraper import Sort, reviews
import cohere

# Setup
COHERE_API_KEY = "4ynfZPaAfQD4L4z6NEwJSWoBlIDltTVMmPtgFeAP"
client = cohere.Client(COHERE_API_KEY)

def fetch_reviews(app_id, num_reviews=100):
    result, _ = reviews(
        app_id,
        lang='en',
        country='us',
        sort=Sort.NEWEST,
        count=num_reviews
    )
    return [r['content'] for r in result]

def summarize_reviews(reviews_list):
    joined_reviews = "\n".join(reviews_list[:100])
    response = client.summarize(text=joined_reviews)
    return response.summary

# Streamlit UI
st.title("📱 App Review Summarizer")
app_id = st.text_input("Enter Google Play App ID (e.g. com.whatsapp)")

if st.button("Summarize"):
    if app_id.strip() == "":
        st.warning("Please enter a valid app ID.")
    else:
        with st.spinner("Fetching and summarizing reviews..."):
            try:
                reviews_list = fetch_reviews(app_id)
                summary = summarize_reviews(reviews_list)
                st.subheader("Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"An error occurred: {e}")
