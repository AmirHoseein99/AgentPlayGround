from fastapi import APIRouter, HTTPException
from agent.agent import agent
from logger import get_logger

agent_router = APIRouter(prefix="/agent", tags=["agent"])


@agent_router.post("/call_agent")
async def call_agent_endpoint(user_input: str, conversation_id: str = None):
    logger = get_logger("agent_api")
    logger.info(f"Received user input: {user_input}, {conversation_id}")

    try:
        response = agent.run(user_input, conversation_id)
        logger.info(f"Agent response: {response}")
        return {"response": response}
    except Exception as e:
        logger.exception("Error calling agent")
        raise HTTPException(status_code=500, detail=str(e))
