from typing import Optional, List
from app.repositories.university_repository import UniversityRepository
from app.models.university import University
from app.models.extracurricular import Extracurricular
from sqlalchemy.orm import Session


def toefl_to_ielts(toefl: float) -> float:
    return round(toefl / 120 * 9, 1)


def _calculate_chance(
    university: University,
    gpa: Optional[float],
    sat: Optional[int],
    ielts: Optional[float],
    toefl: Optional[float],
    extracurriculars: List[Extracurricular],
) -> dict:
    score = 0

    if gpa is not None:
        if gpa >= university.avg_gpa:       score += 40
        elif gpa >= university.min_gpa:     score += 20

    if sat is not None:
        if sat >= university.avg_sat:       score += 30
        elif sat >= university.min_sat:     score += 15

    english_score: Optional[float] = None
    if ielts is not None and toefl is not None:
        english_score = max(ielts, toefl_to_ielts(toefl))
    elif ielts is not None:
        english_score = ielts
    elif toefl is not None:
        english_score = toefl_to_ielts(toefl)

    if english_score is not None:
        if english_score >= university.avg_ielts:   score += 20
        elif english_score >= university.min_ielts: score += 10

    if extracurriculars:
        score += min(len(extracurriculars) * 2, 10)

    probability = round(university.acceptance_rate * (score / 100) * 5 * 100, 1)
    probability = min(probability, 95.0)

    if probability < 5:
        label, color = "Сложно", "red"
    elif probability < 20:
        label, color = "Средне", "yellow"
    else:
        label, color = "Реально", "green"

    return {"probability": probability, "label": label, "color": color}


class UniversityService:
    def __init__(self, db: Session):
        self.repo = UniversityRepository(db)

    def get_all_with_chances(
        self,
        gpa: Optional[float],
        sat: Optional[int],
        ielts: Optional[float],
        toefl: Optional[float],
        extracurriculars: List[Extracurricular],
    ) -> List[dict]:
        universities = self.repo.get_all()
        return [
        {
            "id": u.id,
            "name": u.name,
            "country": u.country,
            "city": u.city,
            "min_gpa": u.min_gpa,
            "min_sat": u.min_sat,
            **_calculate_chance(u, gpa, sat, ielts, toefl, extracurriculars),
        }
        for u in universities
]