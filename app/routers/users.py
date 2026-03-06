from fastapi import APIRouter, Depends, status
from app.models.user import User
from app.schemas.user import UserProfileResponse
from app.services.user_service import UserService
from app.dependencies import get_user_service
from app.auth import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserProfileResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    service.delete_account(current_user)