from pathlib import Path
import os
from dotenv import load_dotenv

# Project directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(ROOT_DIR / ".env")

# Ollama settings
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text"
)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Data directories
DATA_DIR = ROOT_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"

VECTOR_DB_PATH = ROOT_DIR / "vectorstore" / "faiss_index"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DB_PATH.parent.mkdir(parents=True, exist_ok=True)