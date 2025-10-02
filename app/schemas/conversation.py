from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from app.models.conversation import ConversationStatus, MessageType

class MessageBase(BaseModel):
    message: str
    message_type: MessageType = MessageType.text
    offer_price: Optional[Decimal] = None

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: UUID
    conversation_id: UUID
    sender_id: UUID
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ConversationBase(BaseModel):
    product_id: UUID

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: UUID
    buyer_id: UUID
    seller_id: UUID
    status: ConversationStatus
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []

    model_config = ConfigDict(from_attributes=True)