from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from llm.chat_engine import ask_llm, stream_llm

router = APIRouter(prefix="/llm", tags=["llm"])


@router.get("/ask")
def ask_llm_api(user_input: str):
    return ask_llm(user_input=user_input)


@router.get("/stream_llm")
def stream_llm_api(user_input: str):

    return StreamingResponse(stream_llm(user_input), media_type="text/event-stream")
