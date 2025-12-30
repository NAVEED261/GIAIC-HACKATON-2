"""
Phase-5 Chat Endpoint - OpenAI Integration
Simplified chat for task management with Phase-5 advanced features

@author: Phase-5 System
"""

import os
import json
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from openai import OpenAI

from db import get_session
from models.task import Task, TaskCreate, Priority, RecurrencePattern
from models.tag import Tag
from models.reminder import Reminder, ReminderType
from models.conversation import Conversation
from models.message import Message
from middleware.auth import get_current_user
from models.user import User
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: list
    status: str


# OpenAI client
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


# Phase-5 Advanced Functions
OPENAI_FUNCTIONS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task with title, priority, due date, and recurring options",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"], "description": "Task priority"},
                    "is_recurring": {"type": "boolean", "description": "Is this a recurring task?"},
                    "recurrence_pattern": {"type": "string", "enum": ["daily", "weekly", "monthly"], "description": "Recurrence pattern"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List tasks with optional filters",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["all", "active", "completed"], "description": "Filter by status"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"], "description": "Filter by priority"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "Task ID to complete"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "Task ID to delete"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_priority",
            "description": "Set task priority",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "Task ID"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"], "description": "New priority"}
                },
                "required": ["task_id", "priority"]
            }
        }
    }
]


def execute_function(session: Session, user_id: int, function_name: str, args: dict) -> dict:
    """Execute a function and return result"""

    if function_name == "add_task":
        priority = Priority(args.get("priority", "medium"))
        recurrence = None
        if args.get("recurrence_pattern"):
            recurrence = RecurrencePattern(args["recurrence_pattern"])

        task = Task(
            user_id=user_id,
            title=args["title"],
            description=args.get("description"),
            priority=priority,
            is_recurring=args.get("is_recurring", False),
            recurrence_pattern=recurrence
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"success": True, "task_id": task.id, "title": task.title, "priority": task.priority.value}

    elif function_name == "list_tasks":
        query = select(Task).where(Task.user_id == user_id)

        status = args.get("status", "all")
        if status == "active":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        priority = args.get("priority")
        if priority:
            query = query.where(Task.priority == Priority(priority))

        tasks = session.exec(query).all()
        return {
            "success": True,
            "count": len(tasks),
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "completed": t.completed,
                    "priority": t.priority.value,
                    "is_recurring": t.is_recurring
                }
                for t in tasks
            ]
        }

    elif function_name == "complete_task":
        task = session.get(Task, args["task_id"])
        if not task or task.user_id != user_id:
            return {"success": False, "error": "Task not found"}
        task.completed = True
        session.commit()
        return {"success": True, "task_id": task.id, "message": f"Task '{task.title}' completed"}

    elif function_name == "delete_task":
        task = session.get(Task, args["task_id"])
        if not task or task.user_id != user_id:
            return {"success": False, "error": "Task not found"}
        title = task.title
        session.delete(task)
        session.commit()
        return {"success": True, "message": f"Task '{title}' deleted"}

    elif function_name == "set_priority":
        task = session.get(Task, args["task_id"])
        if not task or task.user_id != user_id:
            return {"success": False, "error": "Task not found"}
        task.priority = Priority(args["priority"])
        session.commit()
        return {"success": True, "task_id": task.id, "priority": task.priority.value}

    return {"success": False, "error": "Unknown function"}


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Chat endpoint with OpenAI function calling for task management"""

    client = get_openai_client()
    if not client:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    # Get or create conversation
    if request.conversation_id:
        conversation = session.exec(
            select(Conversation).where(
                Conversation.id == request.conversation_id,
                Conversation.user_id == current_user.id
            )
        ).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=current_user.id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        logger.info(f"Created new conversation {conversation.id} for user {current_user.id}")

    # Fetch conversation history for context
    history_messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
    ).all()

    # Store user message
    user_message = Message(
        conversation_id=conversation.id,
        user_id=current_user.id,
        role="user",
        content=request.message
    )
    session.add(user_message)
    session.commit()
    logger.info(f"Stored user message in conversation {conversation.id}")

    # Build messages with history
    messages = [
        {
            "role": "system",
            "content": """You are a helpful AI assistant for Phase-5 Todo Manager.
You help users manage tasks with advanced features:
- Priority levels (low, medium, high, urgent)
- Recurring tasks (daily, weekly, monthly)
- Tags and categories

Use the provided functions to manage tasks. Be helpful and conversational."""
        }
    ]

    # Add history
    for hist_msg in history_messages:
        messages.append({"role": hist_msg.role, "content": hist_msg.content})

    # Add current message
    messages.append({"role": "user", "content": request.message})

    tools_used = []

    try:
        # First call - let OpenAI decide
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=OPENAI_FUNCTIONS,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        if assistant_message.tool_calls:
            messages.append(assistant_message)

            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                tools_used.append(function_name)
                logger.info(f"Executing function: {function_name} with args: {function_args}")

                result = execute_function(session, current_user.id, function_name, function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(result)
                })

            # Second call for natural response
            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            assistant_response = final_response.choices[0].message.content
        else:
            assistant_response = assistant_message.content

        # Store assistant response
        assistant_msg = Message(
            conversation_id=conversation.id,
            user_id=current_user.id,
            role="assistant",
            content=assistant_response
        )
        session.add(assistant_msg)

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        session.commit()
        logger.info(f"Stored assistant response in conversation {conversation.id}")

        return ChatResponse(
            conversation_id=conversation.id,
            response=assistant_response,
            tool_calls=tools_used,
            status="success"
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
