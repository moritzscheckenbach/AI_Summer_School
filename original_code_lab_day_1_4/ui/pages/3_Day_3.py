import httpx
import streamlit as st

from utils import stream_json

st.set_page_config(page_title="Day 3 - Basic RAG", page_icon="📄")

st.title("Day 3 · Basic RAG (chat)")

if "messages_d3" not in st.session_state:
    st.session_state.messages_d3 = []

for msg in st.session_state.messages_d3:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about the Tesla manual"):
    st.session_state.messages_d3.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    payload = {"messages": st.session_state.messages_d3}
    with st.chat_message("assistant"):
        try:
            stream = stream_json("/api/day3/chat", payload)
            reply = st.write_stream(stream)
        except httpx.HTTPError as exc:
            st.error(f"Backend error: {exc.response.status_code if exc.response else 'unknown'}")
            reply = ""
        except Exception as exc:  # pragma: no cover - defensive
            st.error(f"Unexpected error: {exc}")
            reply = ""
    st.session_state.messages_d3.append({"role": "assistant", "content": reply})
