from typing import Any, Dict, Optional
from fastapi import APIRouter, Form, HTTPException

from app.services.gtts import GoogleTextToSpeech
from app.services.whatsapp import WhatsappService

router = APIRouter()
whatsapp_service = WhatsappService()
gtts_service = GoogleTextToSpeech()

# @router.post("/webhook/whatsapp")
# async def whatsapp_webhook(payload: Dict[str, Any]):
#     """
#         Webhook para receber mensagens do Whatsapp
#     """
#     try:
#         message = await whatsapp_service.process_incoming_message(payload)
#         audio_url = await gtts_service.text_to_speech(message.text)

#         whatsapp_service.send_audio_message(
#             message.sender_id,
#             audio_url
#         )

#         return {"status": "success"}

#     except Exception as e:
#         raise HTTPException(500, detail=str(e))

@router.post("/webhook/whatsapp")
async def whatsapp_webhook(
    MessageSid: str = Form(...),
    From: str = Form(...),
    Body: str = Form(...),
    MediaUrl0: Optional[str] = Form(None)
):
    """
    Webhook para receber mensagens do WhatsApp via Twilio.
    """

    try:
        from_number = From.replace("whatsapp:", "")

        whatsapp_service.send_text_message(from_number, "Carregando, aguarde um momento... ⏳")

        payload = {
            "MessageSid": MessageSid,
            "From": From,
            "Body": Body,
            "MediaUrl0": MediaUrl0
        }
        
        message = await whatsapp_service.process_incoming_message(payload)
        
        audio_url = gtts_service.text_to_speech(message.text)
        
        whatsapp_service.send_audio_message(
            From.replace("whatsapp:", ""),
            await audio_url
        )

        return {"status": "success"}

    except Exception as e:
        raise HTTPException(500, detail=str(e))
