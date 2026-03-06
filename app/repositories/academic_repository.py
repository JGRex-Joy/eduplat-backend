from sqlalchemy.orm import Session
from app.models.academic import AcademicInfo
from app.repositories.base import BaseRepository


class AcademicRepository(BaseRepository[AcademicInfo]):
    def __init__(self, db: Session):
        super().__init__(AcademicInfo, db)

    def get_by_user(self, user_id: int) -> AcademicInfo | None:
        return self.db.query(AcademicInfo).filter(AcademicInfo.user_id == user_id).first()

    def upsert(self, user_id: int, data: dict) -> AcademicInfo:
        academic = self.get_by_user(user_id)

        if academic:
            for field, value in data.items():
                setattr(academic, field, value)
        else:
            academic = AcademicInfo(user_id=user_id, **data)

        return self.save(academic)