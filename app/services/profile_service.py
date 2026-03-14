from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.repositories.user_repository import UserRepository, UserAboutRepository
from app.repositories.academic_repository import AcademicRepository
from app.repositories.extracurricular_repository import ExtracurricularRepository
from app.models.user import User, UserAbout
from app.models.academic import AcademicInfo
from app.models.extracurricular import Extracurricular
from app.schemas.user import UserAboutCreate
from app.schemas.academic import AcademicInfoCreate
from app.schemas.extracurricular import ExtracurricularCreate


class ProfileService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.about_repo = UserAboutRepository(db)
        self.academic_repo = AcademicRepository(db)
        self.extra_repo = ExtracurricularRepository(db)

    #  About 

    def upsert_about(self, current_user: User, payload: UserAboutCreate) -> UserAbout:
        if payload.email and self.user_repo.email_taken_by_other(payload.email, current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Этот email уже используется другим пользователем",
            )
        return self.about_repo.upsert(
            user=current_user,
            name=payload.name,
            school=payload.school,
            grade=payload.grade,
            email=payload.email,
        )

    def get_about(self, user_id: int) -> UserAbout:
        about = self.about_repo.get_by_user(user_id)
        if not about:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Информация не найдена")
        return about

    #  Academic 

    def upsert_academic(self, user_id: int, payload: AcademicInfoCreate) -> AcademicInfo:
        return self.academic_repo.upsert(
            user_id=user_id,
            data=payload.model_dump(exclude_none=True),
        )

    def get_academic(self, user_id: int) -> AcademicInfo:
        academic = self.academic_repo.get_by_user(user_id)
        if not academic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Академическая информация не найдена",
            )
        return academic

    #  Extracurricular 

    def replace_extracurriculars(self, user_id: int, payload: ExtracurricularCreate) -> List[Extracurricular]:
        return self.extra_repo.replace_all(
            user_id=user_id,
            categories=payload.categories,
            years_active=payload.years_active,
        )

    def get_extracurriculars(self, user_id: int) -> List[Extracurricular]:
        return self.extra_repo.get_by_user(user_id)

    def delete_extracurricular(self, entry_id: int, user_id: int) -> None:
        entry = self.extra_repo.get_by_id_and_user(entry_id, user_id)
        if not entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Запись не найдена")
        self.extra_repo.delete(entry)