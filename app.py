"""Streamlit chat UI for the Londiani Worshippers RAG corpus.

Local run:
    export GEMINI_API_KEY=...
    streamlit run app.py

Streamlit Community Cloud:
    Add GEMINI_API_KEY under Settings -> Secrets, e.g.:
        GEMINI_API_KEY = "your-key-here"
"""

import os

import streamlit as st

# Streamlit secrets aren't automatically exported as env vars -- rag/config.py
# reads os.environ, so bridge it here before importing anything from rag/.
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

from rag.qa import answer  # noqa: E402  (must come after the env var is set)

st.set_page_config(page_title="Londiani Worshippers RAG", page_icon="⛪")
st.title("⛪ Londiani Worshippers — Records Assistant")
st.caption(
    "Ask about sermons, board minutes, choir schedules, outreach logs, and other "
    "church records. Answers are grounded only in the indexed corpus."
)

if not os.environ.get("GEMINI_API_KEY"):
    st.error(
        "GEMINI_API_KEY is not set. Add it as a Streamlit secret "
        "(Settings → Secrets) or export it before running locally."
    )
    st.stop()

if not os.path.exists("rag/chroma_db"):
    st.error(
        "No index found at rag/chroma_db. Run `python3 -m rag.ingest` "
        "(or the build-rag-index GitHub Action) to build and commit it first."
    )
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- `{s['doc_id']}` — {s['category'].replace('_', ' ')}")

if question := st.chat_input("Ask a question about the church records..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching records..."):
            result = answer(question)
        st.markdown(result["answer"])
        # de-duplicate sources while preserving order
        seen, sources = set(), []
        for s in result["sources"]:
            if s["doc_id"] not in seen:
                seen.add(s["doc_id"])
                sources.append(s)
        if sources:
            with st.expander("Sources"):
                for s in sources:
                    st.markdown(f"- `{s['doc_id']}` — {s['category'].replace('_', ' ')}")

    st.session_state.messages.append({
        "role": "assistant", "content": result["answer"], "sources": sources,
    })
