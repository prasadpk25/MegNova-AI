from fastapi import APIRouter

from App.ai.chatbot import ask_doctor

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"],
)


@router.post("/")
def chat(question: str):

    answer = ask_doctor(question)

    return {
        "question": question,
        "answer": answer,
    }