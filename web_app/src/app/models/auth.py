from datetime import datetime
from typing import Optional

from sqlalchemy import select, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)

    def hash_password(self) -> None:
        self.password = generate_password_hash(self.password)

    def is_password_valid(self, password) -> bool:
        return check_password_hash(self.password, password)

    @classmethod
    def get_by_email(cls, email: str) -> Optional["User"]:
        result = db.session.execute(select(cls).where(cls.email == email))
        return result.scalars().first()

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class JWTTokenBlockList(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    jti: Mapped[str] = mapped_column(nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    @classmethod
    def get_by_jti(cls, jti: str) -> Optional["JWTTokenBlockList"]:
        result = db.session.execute(select(cls).where(cls.jti == jti))
        return result.scalars().first()

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f"<JWTTokenBlockList(id={self.id}, jti={self.jti}, created_at={self.created_at})>"
