from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Application Configuration
    app_name: str = "Qdrant CUAD Search"
    app_version: str = "2.0.0"
    description: str = "Professional commercial contract search platform powered by Qdrant vector search and the CUAD dataset"
    debug: bool = False
    
    # OpenAI Configuration
    openai_api_key: str
    
    # Qdrant Configuration
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection_name: str = "cuad_contracts_v2"
    
    # CORS Configuration
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "https://qdrant-cuad.vercel.app"
    ]
    
    # Search Configuration
    default_search_limit: int = 20
    max_search_limit: int = 100
    similarity_threshold: float = 0.3
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings() 