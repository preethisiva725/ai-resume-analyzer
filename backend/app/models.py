from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func

from .database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    resume_filename = Column(
        String(255),
        nullable=False
    )

    job_description = Column(
        Text,
        nullable=False
    )

    match_score = Column(
        Float,
        nullable=True
    )

    technical_score = Column(
        Float,
        nullable=True
    )

    soft_skill_score = Column(
        Float,
        nullable=True
    )

    quality_score = Column(
        Float,
        nullable=True
    )

    matching_skills = Column(
        Text,
        nullable=True
    )

    missing_skills = Column(
        Text,
        nullable=True
    )

    suggestions = Column(
        Text,
        nullable=True
    )

    quality_strengths = Column(
        Text,
        nullable=True
    )

    quality_warnings = Column(
        Text,
        nullable=True
    )

    word_count = Column(
        Integer,
        nullable=True
    )

    action_verb_count = Column(
        Integer,
        nullable=True
    )

    quantifiable_achievement_count = Column(
        Integer,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )