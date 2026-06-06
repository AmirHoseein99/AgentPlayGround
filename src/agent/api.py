from fastapi import APIRouter, HTTPException
from .agent import call_agent

agent_router = APIRouter(
    prefix="/agent",
    tags=["agent"]
)

@agent_router.post("/call_agent")
async def call_agent_endpoint(user_input: str):
    try:
        response = call_agent(user_input)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))