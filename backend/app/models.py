from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    technologies: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    github: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        default="#"
    )

    featured: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )

    overview: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    contribution: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    highlights: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

class Experience(Base):
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    role: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    company: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    period: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    technologies: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

class SkillGroup(Base):
    __tablename__ = "skill_groups"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    skills: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
