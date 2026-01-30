from pydantic_settings import BaseSettings
from typing import List
import json
import os
from pathlib import Path

# Find .env file - check current dir, parent dir, and project root
def find_env_file():
    # Try current directory
    if os.path.exists(".env"):
        return ".env"
    # Try parent directory (for when running from backend/)
    if os.path.exists("../.env"):
        return "../.env"
    # Try project root
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        return str(env_path)
    return ".env"  # Default, will fail if not found

class Settings(BaseSettings):
    # Database
    DB_SERVER: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_DRIVER: str = "ODBC Driver 18 for SQL Server"
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    API_TITLE: str = "NYC TLC Trip Analytics API"
    API_VERSION: str = "1.0.0"
    CORS_ORIGINS: str = '["http://localhost:4200"]'
    ALLOWED_ORIGINS: str = ""  # Alternative env var name, takes precedence
    
    @property
    def cors_origins_list(self) -> List[str]:
        # Use ALLOWED_ORIGINS if set, otherwise fall back to CORS_ORIGINS
        origins_str = self.ALLOWED_ORIGINS if self.ALLOWED_ORIGINS else self.CORS_ORIGINS
        
        # Handle "*" for all origins
        if origins_str == "*":
            return ["*"]
        
        # Handle JSON array format
        try:
            return json.loads(origins_str)
        except json.JSONDecodeError:
            # If not valid JSON, treat as single origin
            return [origins_str] if origins_str else ["http://localhost:4200"]
    
    @property
    def database_url(self) -> str:
        return (
            f"DRIVER={{{self.DB_DRIVER}}};"
            f"SERVER={self.DB_SERVER};"
            f"DATABASE={self.DB_NAME};"
            f"UID={self.DB_USER};"
            f"PWD={self.DB_PASSWORD};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
        )
    
    class Config:
        env_file = find_env_file()
        case_sensitive = True

settings = Settings()