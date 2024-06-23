from typing import Optional
from ..extensions import db
from sqlalchemy import select
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column


class Task(db.Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    @classmethod
    def get_by_id(cls, id: int) -> Optional["Task"]:
        return db.session.get(Task, id)

    @classmethod
    def get_all(cls) -> list["Task"]:
        result = db.session.execute(select(Task))
        return result.scalars().all()

    @classmethod
    def get_by_title(cls, title: str) -> Optional["Task"]:
        result = db.session.execute(select(Task).where(Task.title == title))
        return result.scalars().first()
    
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"
