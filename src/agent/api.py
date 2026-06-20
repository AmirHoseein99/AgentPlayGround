from fastapi import APIRouter, HTTPException
from .agent import call_agent
from ..logger import get_logger
from ..memory.json_memory import get_conversation_messages, append_to_conversation

agent_router = APIRouter(prefix="/agent", tags=["agent"])


@agent_router.post("/call_agent")
async def call_agent_endpoint(user_input: str, conversation_id: str = None):
    logger = get_logger("agent_api")
    conversation_history = []
    if conversation_id:
        conversation_history = get_conversation_messages(conversation_id)

    logger.info(f"Received user input: {user_input}, {conversation_id}")
    append_to_conversation(role='user', content=user_input, conversation_id=conversation_id)
    try:
        response = call_agent(user_input, conversation_history, conversation_id)
        logger.info(f"Agent response: {response}")
        return {"response": response}
    except Exception as e:
        logger.exception("Error calling agent")
        raise HTTPException(status_code=500, detail=str(e))
