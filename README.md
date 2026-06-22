# RAG System Action Script

This file explains what to do next with the RAG documentation and chatbot.

1. Review the RAG documentation
   - Open `rag_types.md` to learn the different Retrieval-Augmented Generation (RAG) system types.
   - The document covers sparse, dense, hybrid, RAG-Sequence, RAG-Token, and real-world use cases.

2. Run the chatbot script
   - In PowerShell, run:
     python .\script.py
   - Ask questions like:
     - What is sparse retrieval?
     - Tell me about hybrid RAG.
     - How do RAG-Sequence and RAG-Token differ?
     - What is the difference between sparse and dense retrieval?
     - How can I use RAG for a conversational assistant?

3. Understand the script behavior
   - `script.py` loads `rag_types.md` and splits the document into passages.
   - It uses a simple keyword-based retrieval strategy to find relevant passages.
   - If no matching passage is found, it asks you to keep the question related to the documentation.

4. Extend the system
   - To add real vector search or API-backed embeddings, install Python packages such as `openai`, `sentence-transformers`, or `faiss-cpu`.
   - Then update `rag.py` to embed document passages and search by similarity instead of keyword counts.

5. Optional setup
   - Create a virtual environment:
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
   - Install packages if needed:
     python -m pip install --upgrade pip
     python -m pip install openai sentence-transformers faiss-cpu

6. Notes
   - The current chatbot is designed for local offline use and does not call external APIs.
   - You can change `rag_types.md` anytime to add more RAG system types or examples.

Happy exploring RAG systems!
