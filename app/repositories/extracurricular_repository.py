from sqlalchemy.orm import Session
from typing import List
from app.models.extracurricular import Extracurricular, ExtracurricularCategory
from app.repositories.base import BaseRepository


class ExtracurricularRepository(BaseRepository[Extracurricular]):
    def __init__(self, db: Session):
        super().__init__(Extracurricular, db)

    def get_by_user(self, user_id: int) -> List[Extracurricular]:
        return self.db.query(Extracurricular).filter(Extracurricular.user_id == user_id).all()

    def get_by_id_and_user(self, entry_id: int, user_id: int) -> Extracurricular | None:
        return self.db.query(Extracurricular).filter(
            Extracurricular.id == entry_id,
            Extracurricular.user_id == user_id,
        ).first()

    def replace_all(
        self,
        user_id: int,
        categories: List[ExtracurricularCategory],
        years_active: str | None,
    ) -> List[Extracurricular]:
        self.db.query(Extracurricular).filter(Extracurricular.user_id == user_id).delete()

        entries = [
            Extracurricular(user_id=user_id, category=cat, years_active=years_active)
            for cat in categories
        ]
        self.db.add_all(entries)
        self.db.commit()
        for entry in entries:
            self.db.refresh(entry)
        return entries