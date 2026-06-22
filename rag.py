import os
import sys
import json
try:
    import readline
except ImportError:
    pass
import anthropic
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DOCUMENT_PATH = Path(__file__).with_name("rag_types.md")

SYSTEM_PROMPT = """You are a RAG guide chatbot. Answer questions by using the RAG documentation text as your knowledge base.
If the user asks something outside the document, say you can only answer based on the RAG documentation."""

client = anthropic.Anthropic(base_url=os.getenv("AZURE_BASE_URL"), api_key=os.getenv("AZURE_API_KEY"))


def load_document(path):
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")
    return path.read_text(encoding="utf-8")


def split_passages(text, max_lines=30):
    lines = text.splitlines()
    passages = []
    buffer = []
    for line in lines:
        buffer.append(line)
        if len(buffer) >= max_lines and line.strip() == "":
            passages.append("\n".join(buffer).strip())
            buffer = []
    if buffer:
        passages.append("\n".join(buffer).strip())
    return passages


def find_relevant_passages(question, passages):
    question_lower = question.lower()
    scored = []
    for passage in passages:
        score = 0
        text = passage.lower()
        for token in question_lower.split():
            if token in text:
                score += 1
        scored.append((score, passage))
    scored.sort(reverse=True, key=lambda item: item[0])
    return [p for score, p in scored if score > 0][:3]


def generate_answer(question, relevant_passages, document_text):
    highlighted = "\n\n---\n\n".join(relevant_passages) if relevant_passages else "None found."
    system = (
        f"{SYSTEM_PROMPT}\n\n"
        f"## Full document\n\n{document_text}\n\n"
        f"## Most relevant sections\n\n{highlighted}"
    )

    print("\nBot: ", end="", flush=True)
    with client.messages.stream(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": question}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    print()


def chat_loop(document_text):
    passages = split_passages(document_text)
    print("RAG Types Chatbot")
    print("Type 'exit' or 'quit' to end the chat.")
    print("Ask about RAG system types, retrieval methods, or architectures.")
    print()

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        relevant = find_relevant_passages(question, passages)
        generate_answer(question, relevant, document_text)
        print()


def main():
    try:
        document_text = load_document(DOCUMENT_PATH)
    except FileNotFoundError as error:
        print(error)
        sys.exit(1)

    chat_loop(document_text)


if __name__ == "__main__":
    main()
