from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.database import get_db
from app.api.deps import get_current_active_user
from app.schemas.conversation import Conversation, ConversationCreate, Message, MessageCreate
from app.services.conversation_service import ConversationService
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Conversation, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation_create: ConversationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    conversation = ConversationService.create_conversation(db, conversation_create, current_user.id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return conversation

@router.get("/", response_model=List[Conversation])
async def list_conversations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    conversations = ConversationService.get_user_conversations(db, current_user.id)
    return conversations

@router.get("/{conversation_id}", response_model=Conversation)
async def get_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    conversation = ConversationService.get_conversation(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Mark messages as read
    ConversationService.mark_messages_as_read(db, conversation_id, current_user.id)
    return conversation

@router.post("/{conversation_id}/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
async def send_message(
    conversation_id: UUID,
    message_create: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    message = ConversationService.send_message(db, conversation_id, current_user.id, message_create)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or not authorized"
        )
    return message