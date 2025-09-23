import streamlit as st
from utils import post_json

st.set_page_config(page_title="Day 2 - Reasoning Basics", page_icon="🧠")

st.title("Day 2 · Self-Consistency / Tool-Use / Plan-and-Solve (single input)")

prompt = st.chat_input("Enter a question or task")
if prompt:
    with st.spinner("Calling backend..."):
        data = post_json("/api/day2/echo", {"message": prompt})
    st.write(data.get("reply", "<no reply>"))
