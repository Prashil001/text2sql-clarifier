from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    OLLAMA_MODEL: str = "qwen3:4b"
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    class Config:
        env_file = ".env"

settings = Settings()