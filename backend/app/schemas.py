from datetime import datetime

from pydantic import BaseModel


class AnalysisCreate(BaseModel):

    resume_filename: str

    job_description: str


class AnalysisResponse(BaseModel):

    id: int

    resume_filename: str

    job_description: str

    match_score: float | None

    technical_score: float | None

    soft_skill_score: float | None

    quality_score: float | None

    matching_skills: str | None

    missing_skills: str | None

    suggestions: str | None

    quality_strengths: str | None

    quality_warnings: str | None

    word_count: int | None

    action_verb_count: int | None

    quantifiable_achievement_count: int | None

    required_skills: list[str]

    preferred_skills: list[str]

    general_skills: list[str]

    high_priority_missing_skills: list[str]

    medium_priority_missing_skills: list[str]

    low_priority_missing_skills: list[str]

    recommendations: list[str]

    created_at: datetime | None


    class Config:

        from_attributes = True