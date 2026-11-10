
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from App.auth.dependencies import get_current_user
from App.models.user import User
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
def chat_with_guidelines(
    request: GuidelineRequest,
    current_user: User = Depends(get_current_user),
):
    answer = ask_guideline(request.question)
    return GuidelineResponse(answer=answer)
