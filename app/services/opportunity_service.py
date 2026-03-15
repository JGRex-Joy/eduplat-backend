from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.opportunity_repository import OpportunityRepository
from app.models.opportunity import Opportunity, OpportunityType


class OpportunityService:
    def __init__(self, db: Session):
        self.repo = OpportunityRepository(db)

    def get_all(self, type: Optional[OpportunityType] = None) -> List[Opportunity]:
        return self.repo.get_all(type=type)

    def get_by_id(self, id: int) -> Opportunity:
        opp = self.repo.get_by_id(id)
        if not opp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Возможность не найдена",
            )
        return opp