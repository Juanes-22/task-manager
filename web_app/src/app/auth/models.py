from datetime import datetime
from typing import Optional

from sqlalchemy import select, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)

    roles = relationship("Role", secondary="user_roles", back_populates="users")

    def has_role(self, role: str) -> bool:
        result = db.session.execute(
            select(Role).join(Role.users).where(User.id == self.id, Role.slug == role)
        )
        role = result.scalars().first()
        return role is not None

    def hash_password(self) -> None:
        self.password = generate_password_hash(self.password)

    def is_password_valid(self, password) -> bool:
        return check_password_hash(self.password, password)

    @classmethod
    def get_by_id(cls, id: int) -> Optional["User"]:
        return db.session.get(User, id)

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


class Role(db.Model):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    slug: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    users = relationship("User", secondary="user_roles", back_populates="roles")

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name={self.name}, slug={self.slug})>"


class UserRole(db.Model):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))


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
