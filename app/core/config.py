from datetime import timedelta
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Configurações do Twilio
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_WHATSAPP_NUMBER: str

    # Configurações da aplicação (PODE SER ALTERADOS FUTURAMENTE)
    APP_NAME: str = "Whatsapp TTS Bot"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    STORAGE_BUCKET_NAME: str
    SIGNED_URL_EXPIRATION: timedelta = timedelta(hours=1)
    STORAGE_BUCKET_DESTINATION: str
    STORAGE_CONTENT_TYPE: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()