from fastapi import APIRouter
from pydantic import BaseModel

from App.services.guideline_chat import ask_guideline

router = APIRouter(
    prefix="/clinical-guidelines",
    tags=["Clinical Guidelines"]
)


class GuidelineRequest(BaseModel):
    question: str


class GuidelineResponse(BaseModel):
    answer: str


@router.post("/chat", response_model=GuidelineResponse)
def chat_with_guidelines(request: GuidelineRequest):
    answer = ask_guideline(request.question)
    return GuidelineResponse(answer=answer)