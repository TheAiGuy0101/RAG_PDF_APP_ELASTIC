import streamlit as st
import os
from pdf_processing import process_files_in_parallel
from elasticsearch_utils import index_documents
from retriever import search_documents
from qa_pipeline import answer_question
import logging
from utils import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

st.title("PDF RAG Application")

uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.write("Processing files...")
    if not os.path.exists("data/uploads"):
        os.makedirs("data/uploads")

    file_paths = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join("data/uploads", uploaded_file.name)
        file_paths.append(file_path)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    try:
        texts = process_files_in_parallel(file_paths)
        index_documents(texts)
        st.write("Files processed and indexed.")
    except Exception as e:
        logger.error(f"Error processing files: {e}")
        st.error(f"An error occurred while processing the files: {e}")

    st.title("Q&A Section")
    question = st.text_input("Ask a question")

    if question:
        try:
            # Retrieve relevant documents
            retrieved_docs = search_documents(question)
            context = " ".join(retrieved_docs)
            answer = answer_question(question, context)
            st.write(f"Answer: {answer}")
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            st.error(f"An error occurred while answering the question: {e}")
