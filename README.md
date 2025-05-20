# Walgreens Drug Interaction Checker (RAG-Powered)

This project is an AI-powered Drug Interaction Detection System for Walgreens pharmacists.  
It uses **Retrieval-Augmented Generation (RAG)** to retrieve real FDA drug documents and generate safe, clinical pharmacist-friendly recommendations.

---

## 📦 Project Structure

```bash
drug-interaction-agent/
├── app.py               # Streamlit app frontend
├── agent.py             # Drug search + OpenAI analysis
├── embedding_utils.py   # Chunk PDFs + Build FAISS database
├── create_faiss_db.py    # (Optional) Create FAISS manually
├── patients.csv         # Patient ID + Past Prescription history
├── .env                 # Environment Variables (API keys)
├── README.md            # This file
├── requirements.txt     # Python libraries needed
├── drug_pdfs/           # Uploaded PDF drug documents
├── faiss_drug_db/       # FAISS vector database built from PDFs
