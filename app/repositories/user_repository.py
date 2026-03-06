from sqlalchemy.orm import Session
from app.models.user import User, UserAbout
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, email: str, hashed_password: str) -> User:
        return self.save(User(email=email, hashed_password=hashed_password))

    def email_taken_by_other(self, email: str, current_user_id: int) -> bool:
        return self.db.query(User).filter(
            User.email == email,
            User.id != current_user_id,
        ).first() is not None


class UserAboutRepository(BaseRepository[UserAbout]):
    def __init__(self, db: Session):
        super().__init__(UserAbout, db)

    def get_by_user(self, user_id: int) -> UserAbout | None:
        return self.db.query(UserAbout).filter(UserAbout.user_id == user_id).first()

    def upsert(self, user: User, name=None, school=None, grade=None, email=None) -> UserAbout:
        about = self.get_by_user(user.id)

        if about:
            if name is not None:
                about.name = name
            if school is not None:
                about.school = school
            if grade is not None:
                about.grade = grade
        else:
            about = UserAbout(user_id=user.id, name=name, school=school, grade=grade)

        if email is not None:
            user.email = email

        return self.save(about)