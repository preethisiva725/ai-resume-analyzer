from ..services.skill_priority import (
    classify_job_skills
)


def classify_missing_skills(
    missing_skills: list[str],
    job_description: str
) -> dict:

    priority_result = classify_job_skills(
        missing_skills,
        job_description
    )

    return {
        "high_priority": sorted(
            priority_result["required"]
        ),

        "medium_priority": sorted(
            priority_result["preferred"]
        ),

        "low_priority": sorted(
            priority_result["general"]
        )
    }