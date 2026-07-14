from fastapi import APIRouter
from pydantic import BaseModel

from App.ai.chatbot import ask_doctor

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"],
)


class ChatRequest(BaseModel):
    question: str


@router.post("/")
def chat(request: ChatRequest):

    answer = ask_doctor(request.question)

    return {
        "question": request.question,
        "answer": answer,
    }