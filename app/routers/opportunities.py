from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.models.user import User
from app.models.opportunity import OpportunityType
from app.schemas.opportunity import OpportunityResponse
from app.services.opportunity_service import OpportunityService
from app.auth import get_current_user
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()


def get_opportunity_service(db: Session = Depends(get_db)) -> OpportunityService:
    return OpportunityService(db)


@router.get("/", response_model=List[OpportunityResponse])
def list_opportunities(
    type: Optional[OpportunityType] = Query(default=None, description="Фильтр по типу: internship, volunteering, hackathon"),
    current_user: User = Depends(get_current_user),
    service: OpportunityService = Depends(get_opportunity_service),
):
    return service.get_all(type=type)


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
def get_opportunity(
    opportunity_id: int,
    current_user: User = Depends(get_current_user),
    service: OpportunityService = Depends(get_opportunity_service),
):
    return service.get_by_id(opportunity_id)