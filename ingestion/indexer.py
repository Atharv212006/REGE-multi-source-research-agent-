
from langchain_ollama import OllamaEmbeddings

from langchain_community.vectorstores import FAISS

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import (
    EMBEDDING_MODEL,
    OLLAMA_BASE_URL,
    VECTOR_DB_PATH
)

from ingestion.loaders import load_documents


# Create embedding model
def get_embeddings():

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL
    )

    return embeddings


# Create FAISS database
def build_vectorstore(folder_path):

    # Step 1: Load documents
    documents = load_documents(folder_path)

    if not documents:
        raise ValueError("No documents found!")

    print(f"Loaded {len(documents)} documents/pages")

    # Step 2: Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    # Step 3: Generate embeddings
    embeddings = get_embeddings()

    # Step 4: Create FAISS vector database
    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    # Step 5: Save database
    vectorstore.save_local(str(VECTOR_DB_PATH))

    print("FAISS database created successfully!")

    return vectorstore


# Load existing FAISS database
def load_vectorstore():

    embeddings = get_embeddings()

    vectorstore = FAISS.load_local(
        str(VECTOR_DB_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore
