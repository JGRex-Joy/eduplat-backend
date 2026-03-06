from app.repositories.base import BaseRepository
from app.repositories.user_repository import UserRepository, UserAboutRepository
from app.repositories.academic_repository import AcademicRepository
from app.repositories.extracurricular_repository import ExtracurricularRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "UserAboutRepository",
    "AcademicRepository",
    "ExtracurricularRepository",
]