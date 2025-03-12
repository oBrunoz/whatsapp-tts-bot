import uuid
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from app.core.config import Settings
from app.models.message import Message
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class WhatsappService:
    def __init__(self):
        self.settings = Settings()
        self.client = Client(
            self.settings.TWILIO_ACCOUNT_SID,
            self.settings.TWILIO_AUTH_TOKEN
        )
        self.whatsapp_number = self.settings.TWILIO_WHATSAPP_NUMBER

    async def process_incoming_message(self, payload: Dict[str, Any]) -> Message:
        """
            Processa messagens recebidas do webhook do twilio
        """
        try:
            message_sid = str(uuid.uuid4())
            from_number = payload.get('From', '').replace('whatsapp:', '')
            message_text = payload.get('Body', '')
            media_url = payload.get('MediaUrl0')

            message = await Message.create(
                message_sid,
                from_number,
                message_text,
                # media_url
            )

            logger.info(f"Mensagem processada: {message_sid}")
            return message
        
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            raise

    def send_text_message(self, to_number: str, message: str) -> Optional[str]:
        """
            Envia mensagem de texto via whatsapp
        """
        try:
            if not to_number.startswith("whatsapp:"):
                to_number = f'whatsapp:{to_number}'
            
            message = self.client.messages.create(
                from_=f'whatsapp:{self.whatsapp_number}',
                body=message,
                to=to_number
            )
        
            logger.info(f"Messagem enviada: {message.sid}")
            return message.sid
        
        except TwilioRestException as e:
            logger.error(f"Erro no Twilio ao enviar mensagem: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {str(e)}")
    
    def send_audio_message(self, to_number:str, audio_url:str) -> Optional[str]:
        """
            Envia mensagem de áudio via whatsapp
        """
        try:
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'

            message = self.client.messages.create(
                from_=f'whatsapp:{self.whatsapp_number}',
                media_url=[audio_url],
                to=to_number
            )

            logger.info(f"Áudio enviado: {message.sid}")
            return message.sid

        except TwilioRestException as e:
            logger.error(f"Erro Twilio ao enviar áudio: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Erro ao enviar áudio: {str(e)}")
            raise

    async def check_status(self) -> Dict[str, str]:
        """
            Verifica o status da conexão com Twilio
        """
        try:
            self.client.api.accounts(self.settings.TWILIO_ACCOUNT_SID).fetch()
            return {"status": "status ok."}
        except Exception as e:
            return {"status": "erro no status.", "error": str(e)}