import streamlit as st
from utils import post_json

st.set_page_config(page_title="Day 4 - Advanced RAG + Agents", page_icon="🧭")

st.title("Day 4 · Advanced RAG + Agentic Loop (chat)")

if "messages_d4" not in st.session_state:
    st.session_state.messages_d4 = []

for msg in st.session_state.messages_d4:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question to trigger plan→retrieve→verify"):
    st.session_state.messages_d4.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.spinner("Agent working..."):
        payload = {"messages": st.session_state.messages_d4}
        data = post_json("/api/day4/chat", payload)
    reply = data.get("reply", "<no reply>")
    st.session_state.messages_d4.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
