from app.repositories.base import BaseRepository
from app.repositories.user_repository import UserRepository, UserAboutRepository
from app.repositories.academic_repository import AcademicRepository
from app.repositories.extracurricular_repository import ExtracurricularRepository
from app.repositories.university_repository import UniversityRepository
from app.repositories.opportunity_repository import OpportunityRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "UserAboutRepository",
    "AcademicRepository",
    "ExtracurricularRepository",
    "UniversityRepository",
    "OpportunityRepository",
]