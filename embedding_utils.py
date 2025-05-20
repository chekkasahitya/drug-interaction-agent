# embedding_utils.py

import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

load_dotenv()

def load_pdf_text(pdf_folder_path):
    all_text = ""
    for filename in os.listdir(pdf_folder_path):
        if filename.endswith(".pdf"):
            reader = PdfReader(os.path.join(pdf_folder_path, filename))
            for page in reader.pages:
                all_text += page.extract_text()
    return all_text

def build_faiss_from_pdfs(pdf_folder_path, db_path):
    raw_text = load_pdf_text(pdf_folder_path)
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(raw_text)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_texts(chunks, embedding=embeddings)
    db.save_local(db_path)

def load_faiss_db(db_path):
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)


