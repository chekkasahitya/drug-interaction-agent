from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI


def build_rag_chain():
    vectorstore = FAISS.load_local("faiss_index", OpenAIEmbeddings())
    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0),
        retriever=vectorstore.as_retriever()
    )
    return qa_chain
