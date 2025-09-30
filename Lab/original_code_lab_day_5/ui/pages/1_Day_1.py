import streamlit as st
from utils import post_json

st.set_page_config(page_title="Day 1 - Film Reviewer & Sentiment", page_icon="🎬")

st.title("Day 1 · Multilingual Film Reviewer (single input)")

prompt = st.chat_input("Enter a movie title and language (e.g., 'Inception, de')")
if prompt:
    with st.spinner("Calling backend..."):
        data = post_json("/api/day1/echo", {"message": prompt})
    st.write(data.get("reply", "<no reply>"))
