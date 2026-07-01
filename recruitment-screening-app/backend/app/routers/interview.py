from fastapi import APIRouter

from app.routers.candidates import find_candidate
from app.schemas import InterviewQuestionResponse
from app.services.interview_templates import get_interview_questions

router = APIRouter(prefix="/api", tags=["interview"])


@router.get("/candidates/{candidate_id}/interview-questions", response_model=InterviewQuestionResponse)
def interview_questions(candidate_id: str, level: str = "hr") -> InterviewQuestionResponse:
    candidate = find_candidate(candidate_id)
    return get_interview_questions(candidate_id, candidate.name, level)
