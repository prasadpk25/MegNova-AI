from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from App.ai.chatbot import ask_doctor

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"],
)


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description="Doctor's question",
        examples=[
            "Summarize Rahul Sharma's latest blood report"
        ],
    )


@router.post("/")
def chat(request: ChatRequest):
    """
    Ask the AI assistant a medical question.
    """

    try:
        answer = ask_doctor(request.question)

        return {
            "success": True,
            "question": request.question,
            "answer": answer,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )