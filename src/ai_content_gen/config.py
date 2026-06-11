from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    HUGGINGFACEHUB_API_TOKEN: Optional[str] = None
    DEFAULT_MODEL: str = "gpt2"
    DEVICE: int = -1  # -1 => CPU, 0..N => CUDA device id
    USE_HF_HUB: bool = True
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()

