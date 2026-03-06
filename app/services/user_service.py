from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models.user import User


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def delete_account(self, user: User) -> None:
        self.repo.delete(user)