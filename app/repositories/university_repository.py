from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.university import University
from app.repositories.base import BaseRepository


class UniversityRepository(BaseRepository[University]):
    def __init__(self, db: Session):
        super().__init__(University, db)

    def get_all(self, country: Optional[str] = None) -> List[University]:
        query = self.db.query(University)

        if country:
            query = query.filter(University.country == country)

        return query.order_by(University.ranking).all()

    def get_countries(self) -> List[str]:
        rows = (
            self.db.query(University.country)
            .filter(University.country.isnot(None))
            .distinct()
            .order_by(University.country)
            .all()
        )
        return [row[0] for row in rows]