from app.database import SessionLocal, Base, engine
from app.models.university import University

UNIVERSITIES = [
    {
        "name": "Harvard University",
        "country": "США", "city": "Кембридж",
        "min_gpa": 3.7, "avg_gpa": 3.9,
        "min_sat": 1460, "avg_sat": 1550,
        "min_ielts": 7.0, "avg_ielts": 7.5,
        "acceptance_rate": 0.04, "ranking": 1,
    },
    {
        "name": "MIT",
        "country": "США", "city": "Кембридж",
        "min_gpa": 3.8, "avg_gpa": 4.0,
        "min_sat": 1510, "avg_sat": 1570,
        "min_ielts": 7.0, "avg_ielts": 8.0,
        "acceptance_rate": 0.04, "ranking": 2,
    },
    {
        "name": "Stanford University",
        "country": "США", "city": "Стэнфорд",
        "min_gpa": 3.7, "avg_gpa": 3.95,
        "min_sat": 1490, "avg_sat": 1560,
        "min_ielts": 7.0, "avg_ielts": 7.5,
        "acceptance_rate": 0.04, "ranking": 3,
    },
    {
        "name": "University of Oxford",
        "country": "Великобритания", "city": "Оксфорд",
        "min_gpa": 3.7, "avg_gpa": 3.9,
        "min_sat": 1450, "avg_sat": 1540,
        "min_ielts": 7.0, "avg_ielts": 7.5,
        "acceptance_rate": 0.17, "ranking": 4,
    },
    {
        "name": "University of Cambridge",
        "country": "Великобритания", "city": "Кембридж",
        "min_gpa": 3.7, "avg_gpa": 3.9,
        "min_sat": 1450, "avg_sat": 1540,
        "min_ielts": 7.0, "avg_ielts": 7.5,
        "acceptance_rate": 0.18, "ranking": 5,
    },
    {
        "name": "ETH Zurich",
        "country": "Швейцария", "city": "Цюрих",
        "min_gpa": 3.5, "avg_gpa": 3.8,
        "min_sat": 1400, "avg_sat": 1500,
        "min_ielts": 6.5, "avg_ielts": 7.0,
        "acceptance_rate": 0.27, "ranking": 6,
    },
    {
        "name": "University of Toronto",
        "country": "Канада", "city": "Торонто",
        "min_gpa": 3.3, "avg_gpa": 3.7,
        "min_sat": 1300, "avg_sat": 1430,
        "min_ielts": 6.5, "avg_ielts": 7.0,
        "acceptance_rate": 0.43, "ranking": 7,
    },
    {
        "name": "Yale University",
        "country": "США", "city": "Нью-Хейвен",
        "min_gpa": 3.7, "avg_gpa": 3.95,
        "min_sat": 1460, "avg_sat": 1555,
        "min_ielts": 7.0, "avg_ielts": 7.5,
        "acceptance_rate": 0.05, "ranking": 8,
    },
    {
        "name": "Columbia University",
        "country": "США", "city": "Нью-Йорк",
        "min_gpa": 3.7, "avg_gpa": 3.91,
        "min_sat": 1450, "avg_sat": 1545,
        "min_ielts": 7.0, "avg_ielts": 7.5,
        "acceptance_rate": 0.04, "ranking": 9,
    },
    {
        "name": "Princeton University",
        "country": "США", "city": "Принстон",
        "min_gpa": 3.7, "avg_gpa": 3.9,
        "min_sat": 1450, "avg_sat": 1545,
        "min_ielts": 7.0, "avg_ielts": 7.5,
        "acceptance_rate": 0.04, "ranking": 10,
    },
    {
        "name": "National University of Singapore",
        "country": "Сингапур", "city": "Сингапур",
        "min_gpa": 3.4, "avg_gpa": 3.8,
        "min_sat": 1350, "avg_sat": 1480,
        "min_ielts": 6.5, "avg_ielts": 7.0,
        "acceptance_rate": 0.05, "ranking": 11,
    },
    {
        "name": "University of Melbourne",
        "country": "Австралия", "city": "Мельбурн",
        "min_gpa": 3.2, "avg_gpa": 3.6,
        "min_sat": 1250, "avg_sat": 1380,
        "min_ielts": 6.5, "avg_ielts": 7.0,
        "acceptance_rate": 0.70, "ranking": 12,
    },
    {
        "name": "McGill University",
        "country": "Канада", "city": "Монреаль",
        "min_gpa": 3.3, "avg_gpa": 3.7,
        "min_sat": 1300, "avg_sat": 1430,
        "min_ielts": 6.5, "avg_ielts": 7.0,
        "acceptance_rate": 0.46, "ranking": 13,
    },
    {
        "name": "TU Munich",
        "country": "Германия", "city": "Мюнхен",
        "min_gpa": 3.3, "avg_gpa": 3.7,
        "min_sat": 1200, "avg_sat": 1380,
        "min_ielts": 6.0, "avg_ielts": 6.5,
        "acceptance_rate": 0.50, "ranking": 14,
    },
    {
        "name": "University of British Columbia",
        "country": "Канада", "city": "Ванкувер",
        "min_gpa": 3.2, "avg_gpa": 3.6,
        "min_sat": 1250, "avg_sat": 1390,
        "min_ielts": 6.5, "avg_ielts": 7.0,
        "acceptance_rate": 0.52, "ranking": 15,
    },
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        added = 0
        for u in UNIVERSITIES:
            exists = db.query(University).filter_by(name=u["name"]).first()
            if not exists:
                db.add(University(**u))
                added += 1
        db.commit()
        print(f"✅ Seed завершён — добавлено {added} университетов")
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()