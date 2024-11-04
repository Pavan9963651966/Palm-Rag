import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
os.environ['GROQ_API_KEY'] = GROQ_API_KEY

# Initialize the Groq LLM with API key and desired parameters
llm = ChatGroq(api_key=GROQ_API_KEY, model="llama-3.1-70b-Versatile", temperature=0.7)

# Initialize Hugging Face embeddings with SentenceTransformer model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    chunks = text_splitter.split_text(text)
    return chunks



def get_vector_store(text_chunks):
    
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store



def get_conversational_chain(vector_store):
    memory = ConversationBufferMemory(memory_key = "chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vector_store.as_retriever(), memory=memory)
    return conversation_chain   