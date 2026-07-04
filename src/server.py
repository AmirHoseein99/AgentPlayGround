from fastapi import FastAPI
from llm.api import router as llm_router
from agent.api import agent_router


app = FastAPI()

app.include_router(llm_router, prefix="/api")
app.include_router(agent_router, prefix="/api")
