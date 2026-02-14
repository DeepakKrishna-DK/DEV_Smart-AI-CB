import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Model Selection
    USE_FREE_MODELS = os.getenv("USE_FREE_MODELS", "True").lower() == "true"
    USE_GROQ = os.getenv("USE_GROQ", "True").lower() == "true"
    
    # Models
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    FREE_EMBEDDING_MODEL = os.getenv("FREE_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # RAG Settings
    RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", 2))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    
    # LLM Parameters
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.0))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 600))
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PDF_DIR = os.path.join(BASE_DIR, "pdfs")
    VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_db")
    DATA_DIR = os.path.join(BASE_DIR, "data")
    CACHE_DIR = os.path.join(BASE_DIR, "cache")
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    
    # Ensure directories exist
    @classmethod
    def ensure_dirs(cls):
        for d in [cls.PDF_DIR, cls.VECTOR_DB_DIR, cls.DATA_DIR, cls.CACHE_DIR, cls.LOG_DIR]:
            os.makedirs(d, exist_ok=True)
            # Create subdirs for categories
            if d in [cls.PDF_DIR, cls.VECTOR_DB_DIR]:
                os.makedirs(os.path.join(d, "unified"), exist_ok=True)

# Initialize
Config.ensure_dirs()
