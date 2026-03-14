from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import AuthService
from app.services.profile_service import ProfileService
from app.services.user_service import UserService
from app.services.university_service import UniversityService


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)

def get_profile_service(db: Session = Depends(get_db)) -> ProfileService:
    return ProfileService(db)

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

def get_university_service(db: Session = Depends(get_db)) -> UniversityService:
    return UniversityService(db)