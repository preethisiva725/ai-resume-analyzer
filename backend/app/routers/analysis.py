from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Analysis
from ..schemas import AnalysisCreate, AnalysisResponse

from ..services.document_parser import extract_text

from ..services.matcher import compare_skills

from ..services.resume_quality import (
    analyze_resume_quality
)

from ..services.skill_extractor import (
    extract_skills,
    extract_technical_skills,
    extract_soft_skills
)

from ..services.skill_priority import (
    classify_job_skills
)

from ..services.missing_skill_priority import (
    classify_missing_skills
)

from ..services.resume_recommendations import (
    generate_resume_recommendations
)


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


def analysis_to_response(
    analysis: Analysis
) -> dict:

    job_skills = extract_skills(
        analysis.job_description
    )

    priority_result = classify_job_skills(
        job_skills,
        analysis.job_description
    )

    missing_skills = []

    if analysis.missing_skills:

        missing_skills = [
            skill.strip()
            for skill in analysis.missing_skills.split(",")
            if skill.strip()
        ]

    missing_priority_result = (
        classify_missing_skills(
            missing_skills,
            analysis.job_description
        )
    )

    recommendations = (
        generate_resume_recommendations(
            match_score=(
                analysis.match_score or 0
            ),

            technical_score=(
                analysis.technical_score or 0
            ),

            soft_skill_score=(
                analysis.soft_skill_score or 0
            ),

            quality_score=(
                analysis.quality_score or 0
            ),

            matching_skills=(
                [
                    skill.strip()
                    for skill in (
                        analysis.matching_skills or ""
                    ).split(",")
                    if skill.strip()
                ]
            ),

            missing_skills=missing_skills,

            high_priority_missing_skills=(
                missing_priority_result[
                    "high_priority"
                ]
            ),

            medium_priority_missing_skills=(
                missing_priority_result[
                    "medium_priority"
                ]
            ),

            low_priority_missing_skills=(
                missing_priority_result[
                    "low_priority"
                ]
            ),

            quality_strengths=(
                [
                    item.strip()
                    for item in (
                        analysis.quality_strengths or ""
                    ).split("\n")
                    if item.strip()
                ]
            ),

            quality_warnings=(
                [
                    item.strip()
                    for item in (
                        analysis.quality_warnings or ""
                    ).split("\n")
                    if item.strip()
                ]
            ),

            word_count=(
                analysis.word_count or 0
            ),

            action_verb_count=(
                analysis.action_verb_count or 0
            ),

            quantifiable_achievement_count=(
                analysis.quantifiable_achievement_count
                or 0
            )
        )
    )

    return {

        "id": analysis.id,

        "resume_filename":
            analysis.resume_filename,

        "job_description":
            analysis.job_description,

        "match_score":
            analysis.match_score,

        "technical_score":
            analysis.technical_score,

        "soft_skill_score":
            analysis.soft_skill_score,

        "quality_score":
            analysis.quality_score,

        "matching_skills":
            analysis.matching_skills,

        "missing_skills":
            analysis.missing_skills,

        "suggestions":
            analysis.suggestions,

        "quality_strengths":
            analysis.quality_strengths,

        "quality_warnings":
            analysis.quality_warnings,

        "word_count":
            analysis.word_count,

        "action_verb_count":
            analysis.action_verb_count,

        "quantifiable_achievement_count":
            analysis.quantifiable_achievement_count,

        "required_skills":
            priority_result[
                "required"
            ],

        "preferred_skills":
            priority_result[
                "preferred"
            ],

        "general_skills":
            priority_result[
                "general"
            ],

        "high_priority_missing_skills":
            missing_priority_result[
                "high_priority"
            ],

        "medium_priority_missing_skills":
            missing_priority_result[
                "medium_priority"
            ],

        "low_priority_missing_skills":
            missing_priority_result[
                "low_priority"
            ],

        "recommendations":
            recommendations,

        "created_at":
            analysis.created_at
    }


@router.post(
    "/",
    response_model=AnalysisResponse
)
def create_analysis(
    analysis_data: AnalysisCreate,
    db: Session = Depends(get_db)
):

    job_description = (
        analysis_data.job_description
    )

    resume_filename = (
        analysis_data.resume_filename
    )

    resume_path = (
        "uploads/"
        + resume_filename
    )

    try:

        resume_text = extract_text(
            resume_path
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Could not read resume: {error}"
            )
        )

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )

    technical_resume_skills = (
        extract_technical_skills(
            resume_text
        )
    )

    technical_job_skills = (
        extract_technical_skills(
            job_description
        )
    )

    soft_resume_skills = (
        extract_soft_skills(
            resume_text
        )
    )

    soft_job_skills = (
        extract_soft_skills(
            job_description
        )
    )

    match_result = compare_skills(
        resume_skills,
        job_skills,
        job_description
    )

    technical_match_result = (
        compare_skills(
            technical_resume_skills,
            technical_job_skills,
            job_description
        )
    )

    soft_match_result = (
        compare_skills(
            soft_resume_skills,
            soft_job_skills,
            job_description
        )
    )

    suggestions = []

    if match_result[
        "missing_skills"
    ]:

        for skill in match_result[
            "missing_skills"
        ]:

            suggestions.append(
                f"If you have {skill}, "
                f"consider adding it to your "
                f"resume with specific evidence. "
                f"If you do not have it, consider "
                f"learning it."
            )

    if not suggestions:

        suggestions.append(
            "Your resume covers the detected "
            "job skills well."
        )

    quality_result = (
        analyze_resume_quality(
            resume_text
        )
    )

    matching_skills_text = ", ".join(
        match_result[
            "matching_skills"
        ]
    )

    missing_skills_text = ", ".join(
        match_result[
            "missing_skills"
        ]
    )

    suggestions_text = "\n".join(
        suggestions
    )

    quality_strengths_text = "\n".join(
        quality_result[
            "strengths"
        ]
    )

    quality_warnings_text = "\n".join(
        quality_result[
            "warnings"
        ]
    )

    new_analysis = Analysis(

        resume_filename=(
            resume_filename
        ),

        job_description=(
            job_description
        ),

        match_score=(
            match_result[
                "match_score"
            ]
        ),

        technical_score=(
            technical_match_result[
                "technical_score"
            ]
        ),

        soft_skill_score=(
            soft_match_result[
                "soft_score"
            ]
        ),

        quality_score=(
            quality_result[
                "quality_score"
            ]
        ),

        matching_skills=(
            matching_skills_text
        ),

        missing_skills=(
            missing_skills_text
        ),

        suggestions=(
            suggestions_text
        ),

        quality_strengths=(
            quality_strengths_text
        ),

        quality_warnings=(
            quality_warnings_text
        ),

        word_count=(
            quality_result[
                "word_count"
            ]
        ),

        action_verb_count=(
            quality_result[
                "action_verb_count"
            ]
        ),

        quantifiable_achievement_count=(
            quality_result[
                "quantifiable_achievement_count"
            ]
        )
    )

    db.add(
        new_analysis
    )

    db.commit()

    db.refresh(
        new_analysis
    )

    return analysis_to_response(
        new_analysis
    )


@router.get(
    "/",
    response_model=list[AnalysisResponse]
)
def get_analyses(
    db: Session = Depends(get_db)
):

    analyses = (
        db.query(Analysis)
        .order_by(
            Analysis.created_at.desc()
        )
        .all()
    )

    return [
        analysis_to_response(
            analysis
        )
        for analysis in analyses
    ]


@router.get(
    "/{analysis_id}",
    response_model=AnalysisResponse
)
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):

    analysis = (
        db.query(Analysis)
        .filter(
            Analysis.id == analysis_id
        )
        .first()
    )

    if not analysis:

        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )

    return analysis_to_response(
        analysis
    )


@router.delete(
    "/{analysis_id}"
)
def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):

    analysis = (
        db.query(Analysis)
        .filter(
            Analysis.id == analysis_id
        )
        .first()
    )

    if not analysis:

        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )

    db.delete(
        analysis
    )

    db.commit()

    return {
        "message":
            "Analysis deleted successfully."
    }


@router.delete(
    "/"
)
def delete_all_analyses(
    db: Session = Depends(get_db)
):

    db.query(
        Analysis
    ).delete()

    db.commit()

    return {
        "message":
            "All analyses deleted successfully."
    }