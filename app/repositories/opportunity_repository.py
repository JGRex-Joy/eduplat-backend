from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.opportunity import Opportunity, OpportunityType
from app.repositories.base import BaseRepository


class OpportunityRepository(BaseRepository[Opportunity]):
    def __init__(self, db: Session):
        super().__init__(Opportunity, db)

    def get_all(self, type: Optional[OpportunityType] = None) -> List[Opportunity]:
        query = self.db.query(Opportunity)
        if type:
            query = query.filter(Opportunity.type == type)
        return query.order_by(Opportunity.created_at.desc()).all()
