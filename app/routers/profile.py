from fastapi import APIRouter, Depends, status
from typing import List
from app.models.user import User
from app.schemas.user import UserAboutCreate, UserAboutResponse
from app.schemas.academic import AcademicInfoCreate, AcademicInfoResponse
from app.schemas.extracurricular import ExtracurricularCreate, ExtracurricularResponse
from app.services.profile_service import ProfileService
from app.dependencies import get_profile_service
from app.auth import get_current_user

router = APIRouter()


@router.post("/about", response_model=UserAboutResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_about(
    payload: UserAboutCreate,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    return service.upsert_about(current_user, payload)


@router.get("/about", response_model=UserAboutResponse)
def get_about(
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    return service.get_about(current_user.id)


@router.post("/academic", response_model=AcademicInfoResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_academic(
    payload: AcademicInfoCreate,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    return service.upsert_academic(current_user.id, payload)


@router.get("/academic", response_model=AcademicInfoResponse)
def get_academic(
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    return service.get_academic(current_user.id)


@router.post("/extracurricular", response_model=List[ExtracurricularResponse], status_code=status.HTTP_201_CREATED)
def create_extracurriculars(
    payload: ExtracurricularCreate,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    return service.replace_extracurriculars(current_user.id, payload)


@router.get("/extracurricular", response_model=List[ExtracurricularResponse])
def get_extracurriculars(
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    return service.get_extracurriculars(current_user.id)


@router.delete("/extracurricular/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_extracurricular(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    service.delete_extracurricular(entry_id, current_user.id)