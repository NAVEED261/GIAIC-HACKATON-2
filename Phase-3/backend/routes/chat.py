"""
Chat Endpoint

POST /api/{user_id}/chat - Main chat endpoint for todo management

@specs/phase-3-overview.md - Chat API Specification
"""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from sqlmodel import Session

from db import get_session
from agents import (
    AuthAgent, ConversationAgent, ToolRouterAgent,
    TaskManagerAgent, ErrorHandlingAgent
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    """Chat request model"""
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    """Chat response model"""
    conversation_id: int
    response: str
    tool_calls: list
    status: str


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: int,
    request: ChatRequest,
    authorization: str = Header(...),
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint for todo management.

    Workflow:
    1. AuthAgent validates token
    2. ConversationAgent fetches context
    3. ToolRouterAgent selects tools
    4. TaskManagerAgent executes tools
    5. ConversationAgent stores response
    6. Return response to client
    """
    try:
        # Extract token
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid token format")
        token = authorization[7:]

        # 1. AuthAgent: Validate token
        auth_result = AuthAgent.validate_token(token)
        if not auth_result:
            raise HTTPException(status_code=401, detail="Invalid token")

        token_user_id = auth_result["user_id"]

        # 2. AuthAgent: Verify user ownership
        if not AuthAgent.verify_user_ownership(token_user_id, user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        logger.info(f"Authenticated user {user_id}")

        # 3. ConversationAgent: Get or create conversation
        conv_result = await ConversationAgent.get_or_create_conversation(
            session,
            user_id,
            request.conversation_id
        )
        conversation_id = conv_result["conversation_id"]

        # 4. ConversationAgent: Fetch message history
        history = await ConversationAgent.fetch_message_history(
            session,
            conversation_id
        )

        # 5. ConversationAgent: Store user message
        await ConversationAgent.store_user_message(
            session,
            conversation_id,
            user_id,
            request.message
        )

        # 6. ToolRouterAgent: Parse intent
        intent_result = await ToolRouterAgent.parse_intent(
            request.message,
            history
        )

        if intent_result.get("error"):
            logger.error(f"Intent parsing failed: {intent_result['error']}")
            raise Exception(intent_result["error"])

        intent = intent_result.get("action", "unknown")
        params = intent_result.get("params", {})

        # 7. ToolRouterAgent: Select tools
        tools = await ToolRouterAgent.select_tools(intent, params)

        # 8. TaskManagerAgent: Execute tools
        tool_results = await TaskManagerAgent.execute_tools(
            session,
            user_id,
            tools
        )

        # 9. ToolRouterAgent: Generate response
        assistant_response = await ToolRouterAgent.generate_response(
            request.message,
            tool_results,
            history
        )

        # 10. ConversationAgent: Store assistant response
        await ConversationAgent.store_assistant_message(
            session,
            conversation_id,
            user_id,
            assistant_response
        )

        logger.info(f"Chat completed for user {user_id}")

        return ChatResponse(
            conversation_id=conversation_id,
            response=assistant_response,
            tool_calls=[t["tool"] for t in tools],
            status="success"
        )

    except HTTPException:
        raise
    except Exception as e:
        # ErrorHandlingAgent: Handle exception
        error_response = ErrorHandlingAgent.handle_error(e)
        logger.error(f"Chat endpoint error: {error_response}")
        raise HTTPException(status_code=500, detail=error_response["message"])
