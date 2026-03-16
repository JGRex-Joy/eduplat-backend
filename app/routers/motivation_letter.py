from fastapi import APIRouter, Depends
from app.models.user import User
from app.schemas.motivation_letter import MotivationLetterRequest, MotivationLetterResponse
from app.services.motivation_letter_service import MotivationLetterService
from app.auth import get_current_user

router = APIRouter()


def get_motivation_letter_service() -> MotivationLetterService:
    return MotivationLetterService()


@router.post("/analyze", response_model=MotivationLetterResponse)
def analyze_motivation_letter(
    payload: MotivationLetterRequest,
    current_user: User = Depends(get_current_user),
    service: MotivationLetterService = Depends(get_motivation_letter_service),
):
    return service.analyze(payload)