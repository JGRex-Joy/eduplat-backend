from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.models.user import User
from app.schemas.university import UniversityWithChanceResponse
from app.services.university_service import UniversityService
from app.dependencies import get_university_service
from app.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[UniversityWithChanceResponse])
def get_universities(
    country: Optional[str] = Query(default=None, description="Фильтр по стране: США, Канада, ..."),
    label: Optional[str] = Query(default=None, description="Фильтр по сложности: Сложно | Средне | Реально"),
    sort_by: str = Query(default="ranking", description="Сортировка: ranking | min_gpa | min_sat | min_ielts | probability"),
    sort_order: str = Query(default="asc", description="asc | desc"),
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
        country=country,
        label=label,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/countries", response_model=List[str])
def get_countries(
    current_user: User = Depends(get_current_user),
    service: UniversityService = Depends(get_university_service),
):
    return service.get_countries()