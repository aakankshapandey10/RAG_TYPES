import os
import anthropic
import streamlit as st
from pathlib import Path

DOCUMENT_PATH = Path(__file__).with_name("rag_types.md")

client = anthropic.Anthropic(base_url=os.getenv("AZURE_BASE_URL"), api_key=os.getenv("AZURE_API_KEY"))

SYSTEM_PROMPT = """You are a RAG guide chatbot. Answer questions using the RAG documentation as your knowledge base.
If the user asks something outside the document, say you can only answer based on the RAG documentation."""


@st.cache_data
def load_document():
    if not DOCUMENT_PATH.exists():
        return None
    return DOCUMENT_PATH.read_text(encoding="utf-8")


def split_passages(text, max_lines=30):
    lines = text.splitlines()
    passages, buffer = [], []
    for line in lines:
        buffer.append(line)
        if len(buffer) >= max_lines and line.strip() == "":
            passages.append("\n".join(buffer).strip())
            buffer = []
    if buffer:
        passages.append("\n".join(buffer).strip())
    return passages


def find_relevant_passages(question, passages, max_results=3):
    tokens = set(question.lower().split())
    scored = [(sum(1 for t in tokens if t in p.lower()), p) for p in passages]
    scored.sort(reverse=True, key=lambda x: x[0])
    return [p for score, p in scored if score > 0][:max_results]


def stream_answer(question, relevant_passages, document_text):
    highlighted = "\n\n---\n\n".join(relevant_passages) if relevant_passages else "None found."
    system = (
        f"{SYSTEM_PROMPT}\n\n"
        f"## Full document\n\n{document_text}\n\n"
        f"## Most relevant sections\n\n{highlighted}"
    )
    with client.messages.stream(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": question}],
    ) as stream:
        for text in stream.text_stream:
            yield text


# --- Layout ---
st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("RAG Types Chatbot")

document_text = load_document()

if document_text is None:
    st.error(f"Document not found: {DOCUMENT_PATH}")
    st.stop()

doc_col, chat_col = st.columns([1, 1])

with doc_col:
    st.subheader("Document")
    st.markdown(document_text)

with chat_col:
    st.subheader("Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask about RAG types...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        passages = split_passages(document_text)
        relevant = find_relevant_passages(question, passages)

        with st.chat_message("assistant"):
            response = st.write_stream(stream_answer(question, relevant, document_text))

        st.session_state.messages.append({"role": "assistant", "content": response})
