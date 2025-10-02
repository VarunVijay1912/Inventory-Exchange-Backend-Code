from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from app.models.conversation import Conversation, Message
from app.models.product import Product
from app.schemas.conversation import ConversationCreate, MessageCreate
from typing import Optional, List
from uuid import UUID

class ConversationService:
    @staticmethod
    def create_conversation(db: Session, conversation_create: ConversationCreate, buyer_id: UUID) -> Optional[Conversation]:
        # Get product and seller info
        product = db.query(Product).filter(Product.id == conversation_create.product_id).first()
        if not product:
            return None
        
        # Check if conversation already exists
        existing = db.query(Conversation).filter(
            and_(
                Conversation.product_id == conversation_create.product_id,
                Conversation.buyer_id == buyer_id,
                Conversation.seller_id == product.seller_id
            )
        ).first()
        
        if existing:
            return existing
        
        db_conversation = Conversation(
            product_id=conversation_create.product_id,
            buyer_id=buyer_id,
            seller_id=product.seller_id
        )
        db.add(db_conversation)
        db.commit()
        db.refresh(db_conversation)
        return db_conversation

    @staticmethod
    def get_user_conversations(db: Session, user_id: UUID) -> List[Conversation]:
        return db.query(Conversation).filter(
            or_(
                Conversation.buyer_id == user_id,
                Conversation.seller_id == user_id
            )
        ).options(
            joinedload(Conversation.product),
            joinedload(Conversation.buyer),
            joinedload(Conversation.seller),
            joinedload(Conversation.messages)
        ).all()

    @staticmethod
    def get_conversation(db: Session, conversation_id: UUID, user_id: UUID) -> Optional[Conversation]:
        return db.query(Conversation).filter(
            and_(
                Conversation.id == conversation_id,
                or_(
                    Conversation.buyer_id == user_id,
                    Conversation.seller_id == user_id
                )
            )
        ).options(
            joinedload(Conversation.messages),
            joinedload(Conversation.product)
        ).first()

    @staticmethod
    def send_message(db: Session, conversation_id: UUID, sender_id: UUID, message_create: MessageCreate) -> Optional[Message]:
        # Verify user is part of conversation
        conversation = db.query(Conversation).filter(
            and_(
                Conversation.id == conversation_id,
                or_(
                    Conversation.buyer_id == sender_id,
                    Conversation.seller_id == sender_id
                )
            )
        ).first()
        
        if not conversation:
            return None
        
        db_message = Message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            **message_create.model_dump()
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

    @staticmethod
    def mark_messages_as_read(db: Session, conversation_id: UUID, user_id: UUID):
        # Mark messages as read where user is the receiver
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            return
        
        db.query(Message).filter(
            and_(
                Message.conversation_id == conversation_id,
                Message.sender_id != user_id,
                Message.is_read == False
            )
        ).update({"is_read": True})
        db.commit()