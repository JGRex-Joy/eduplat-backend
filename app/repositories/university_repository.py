from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.university import University
from app.repositories.base import BaseRepository


class UniversityRepository(BaseRepository[University]):
    def __init__(self, db: Session):
        super().__init__(University, db)

    def get_all(self) -> List[University]:
        return self.db.query(University).order_by(University.ranking).all()

    def get_by_id(self, university_id: int) -> Optional[University]:
        return self.db.query(University).filter(University.id == university_id).first()