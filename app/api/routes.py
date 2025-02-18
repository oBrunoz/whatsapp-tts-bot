from typing import Any, Dict
from fastapi import APIRouter

router = APIRouter()

@router.post("/webhook/whatsapp")
async def whatsapp_webhook(payload: Dict[str, Any]):
    """
        Webhook para receber mensagens do Whatsapp
    """
    ...