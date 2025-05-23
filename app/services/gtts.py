from app.services.storage import StorageService
from google.cloud import texttospeech
from app.core.config import Settings
from google.api_core import retry
from typing import Optional
import logging
import uuid
import os

logger = logging.getLogger(__name__)

class GoogleTextToSpeech():
    def __init__(self):
        self.settings = Settings()

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        self.client = texttospeech.TextToSpeechClient()
        self.storage = StorageService()

        self.default_language = "pt-BR"
        self.default_voice = "pt-BR-Neural2-B"
        self.default_gender = texttospeech.SsmlVoiceGender.MALE
    
    @retry.AsyncRetry()
    async def text_to_speech(self, text:str, language_code:str = None, voice_name:str = None, gender: texttospeech.SsmlVoiceGender = None) -> Optional[str]:
        """
            gTTs: Converte texto em áudio e retorna a URL do arquivo armazenado
        """
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)

            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code or self.default_language,
                name=voice_name or self.default_voice,
                ssml_gender=gender or self.default_gender
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = self.client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
            
            file_name = f"/audio_{uuid.uuid4()}.mp3"
            temp_path = f"/tmp{file_name}"

            with open(temp_path, 'wb') as out:
                out.write(response.audio_content)

            destination_path = f"{self.settings.STORAGE_BUCKET_DESTINATION.rstrip('/')}{file_name}"

            audio_url = await self.storage.upload_cs_file(
                temp_path,
                destination_path,
                self.settings.STORAGE_CONTENT_TYPE
            )

            os.remove(temp_path)

            logger.info(f"Áudio gerado com sucesso: {file_name}")
            return audio_url
        
        except Exception as e:
            logger.error(f"Erro ao gerar áudio: {str(e)}")
            raise