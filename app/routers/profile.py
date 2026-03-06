from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter()


@router.post("/about", response_model=schemas.UserAboutResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_about(
    payload: schemas.UserAboutCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create or update 'About me' info (Напиши о себе).
    Updates email on the user record if provided.
    """
    about = db.query(models.UserAbout).filter(models.UserAbout.user_id == current_user.id).first()

    if about:
        for field, value in payload.model_dump(exclude_none=True, exclude={"email"}).items():
            setattr(about, field, value)
    else:
        about = models.UserAbout(
            user_id=current_user.id,
            name=payload.name,
            school=payload.school,
            grade=payload.grade,
        )
        db.add(about)


    if payload.email:
        existing = db.query(models.User).filter(
            models.User.email == payload.email,
            models.User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Этот email уже используется другим пользователем"
            )
        current_user.email = payload.email

    db.commit()
    db.refresh(about)
    return about


@router.get("/about", response_model=schemas.UserAboutResponse)
def get_about(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    about = db.query(models.UserAbout).filter(models.UserAbout.user_id == current_user.id).first()
    if not about:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Информация не найдена")
    return about


@router.post("/academic", response_model=schemas.AcademicInfoResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_academic(
    payload: schemas.AcademicInfoCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create or update academic info (Академическая информация).
    """
    academic = db.query(models.AcademicInfo).filter(models.AcademicInfo.user_id == current_user.id).first()

    if academic:
        for field, value in payload.model_dump(exclude_none=True).items():
            setattr(academic, field, value)
    else:
        academic = models.AcademicInfo(
            user_id=current_user.id,
            **payload.model_dump(exclude_none=True)
        )
        db.add(academic)

    db.commit()
    db.refresh(academic)
    return academic


@router.get("/academic", response_model=schemas.AcademicInfoResponse)
def get_academic(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    academic = db.query(models.AcademicInfo).filter(models.AcademicInfo.user_id == current_user.id).first()
    if not academic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Академическая информация не найдена")
    return academic


@router.post("/extracurricular", response_model=List[schemas.ExtracurricularResponse], status_code=status.HTTP_201_CREATED)
def create_extracurriculars(
    payload: schemas.ExtracurricularCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set extracurricular activities (Внеучебная информация).
    Replaces all existing entries for the user.
    """
    db.query(models.Extracurricular).filter(
        models.Extracurricular.user_id == current_user.id
    ).delete()

    new_entries = [
        models.Extracurricular(
            user_id=current_user.id,
            category=category,
            years_active=payload.years_active,
        )
        for category in payload.categories
    ]
    db.add_all(new_entries)
    db.commit()
    for entry in new_entries:
        db.refresh(entry)
    return new_entries


@router.get("/extracurricular", response_model=List[schemas.ExtracurricularResponse])
def get_extracurriculars(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(models.Extracurricular).filter(
        models.Extracurricular.user_id == current_user.id
    ).all()


@router.delete("/extracurricular/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_extracurricular(
    entry_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entry = db.query(models.Extracurricular).filter(
        models.Extracurricular.id == entry_id,
        models.Extracurricular.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Запись не найдена")
    db.delete(entry)
    db.commit()