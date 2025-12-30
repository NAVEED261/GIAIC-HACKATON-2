"""
Conversations Route - Phase-5
Endpoints for chat history management

GET /api/conversations - List all user conversations
GET /api/conversations/{id} - Get conversation with messages
GET /api/conversations/{id}/messages - Get paginated messages
DELETE /api/conversations/{id} - Delete conversation
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from db import get_session
from models import Conversation, Message, User
from middleware.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


@router.get("/")
async def list_conversations(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List all conversations for the current user"""
    try:
        conversations = session.exec(
            select(Conversation)
            .where(Conversation.user_id == current_user.id)
            .order_by(Conversation.updated_at.desc())
        ).all()

        result = []
        for conv in conversations:
            # Get message count and preview
            messages = session.exec(
                select(Message)
                .where(Message.conversation_id == conv.id)
                .order_by(Message.created_at.desc())
            ).all()

            preview = messages[0].content[:50] if messages else "No messages"

            result.append({
                "id": conv.id,
                "user_id": conv.user_id,
                "message_count": len(messages),
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat(),
                "preview": preview
            })

        return {
            "user_id": current_user.id,
            "total": len(result),
            "conversations": result
        }

    except Exception as e:
        logger.error(f"Error listing conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get conversation with all messages"""
    try:
        conversation = session.exec(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id
            )
        ).first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        ).all()

        formatted_messages = [
            {
                "id": msg.id,
                "conversation_id": msg.conversation_id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]

        return {
            "id": conversation.id,
            "user_id": conversation.user_id,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "message_count": len(messages),
            "messages": formatted_messages
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get paginated messages from a conversation"""
    try:
        # Verify ownership
        conversation = session.exec(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id
            )
        ).first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .offset(skip)
            .limit(limit)
        ).all()

        formatted_messages = [
            {
                "id": msg.id,
                "conversation_id": msg.conversation_id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]

        return {
            "conversation_id": conversation_id,
            "skip": skip,
            "limit": limit,
            "total": len(formatted_messages),
            "messages": formatted_messages
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a conversation and all its messages"""
    try:
        conversation = session.exec(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id
            )
        ).first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Delete messages first
        messages = session.exec(
            select(Message).where(Message.conversation_id == conversation_id)
        ).all()

        for msg in messages:
            session.delete(msg)

        # Delete conversation
        session.delete(conversation)
        session.commit()

        logger.info(f"Deleted conversation {conversation_id} with {len(messages)} messages")

        return {
            "status": "success",
            "message": "Conversation deleted successfully",
            "conversation_id": conversation_id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
