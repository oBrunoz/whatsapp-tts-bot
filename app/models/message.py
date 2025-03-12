from typing import Any, Dict, Optional
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.session import async_session
from app.db.base import Base

class Message(Base):
    """Modelo para armazenar mensagens do whatsapp."""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    message_sid = Column(String(64), unique=True, index=True)
    sender_id = Column(String(64), index=True)
    text = Column(Text, nullable=True)
    media_url = Column(String(512), nullable=True)
    status = Column(String(32), default="received")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @classmethod
    async def create(cls, message_sid: str, sender_id: str, text: Optional[str] = None, media_url: Optional[str] = None) -> "Message":
        message = cls(
            message_sid=message_sid,
            sender_id=sender_id,
            text=text,
            media_url=media_url if media_url else "0"
        )

        async with async_session() as session:
            session.add(message)
            await session.commit()
            await session.refresh(message)
        
        return message

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o objeto mensagem em um dicionário
        """
        return {
            "id": self.id,
            "message_sid": self.message_sid,
            "sender_id": self.sender_id,
            "text": self.text,
            "media_url": self.media_url,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }