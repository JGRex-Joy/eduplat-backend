from fastapi import APIRouter, Depends
from typing import List
from app.models.user import User
from app.schemas.university import UniversityWithChanceResponse
from app.services.university_service import UniversityService
from app.dependencies import get_university_service
from app.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[UniversityWithChanceResponse])
def get_universities(
    current_user: User = Depends(get_current_user),
    service: UniversityService = Depends(get_university_service),
):
    academic = current_user.academic_info
    extracurriculars = current_user.extracurriculars

    return service.get_all_with_chances(
        gpa=academic.gpa if academic else None,
        sat=academic.sat if academic else None,
        ielts=academic.ielts if academic else None,
        toefl=academic.toefl if academic else None,
        extracurriculars=extracurriculars or [],
    )