from typing import List


def generate_resume_recommendations(
    match_score: float,
    technical_score: float,
    soft_skill_score: float,
    quality_score: float,
    matching_skills: List[str],
    missing_skills: List[str],
    high_priority_missing_skills: List[str],
    medium_priority_missing_skills: List[str],
    low_priority_missing_skills: List[str],
    quality_strengths: List[str],
    quality_warnings: List[str],
    word_count: int,
    action_verb_count: int,
    quantifiable_achievement_count: int
) -> List[str]:

    recommendations = []


    # --------------------------------------------------
    # Overall Match
    # --------------------------------------------------

    if match_score < 50:

        recommendations.append(
            "Your resume has a low skill match with the job description. "
            "Review the missing skills and tailor your resume to the "
            "requirements that genuinely match your experience."
        )

    elif match_score < 75:

        recommendations.append(
            "Your resume has a moderate skill match. "
            "Focus on the highest-priority missing skills and make "
            "relevant experience more visible."
        )

    else:

        recommendations.append(
            "Your resume has a strong skill match. "
            "Focus on presenting your strongest relevant experience "
            "clearly and supporting it with measurable results."
        )


    # --------------------------------------------------
    # High Priority Missing Skills
    # --------------------------------------------------

    if high_priority_missing_skills:

        skills = ", ".join(
            high_priority_missing_skills
        )

        recommendations.append(
            f"High-priority missing skills: {skills}. "
            "If you genuinely have these skills, add them to the "
            "appropriate resume sections and support them with evidence. "
            "If you do not have them, consider learning them."
        )


    # --------------------------------------------------
    # Medium Priority Missing Skills
    # --------------------------------------------------

    if medium_priority_missing_skills:

        skills = ", ".join(
            medium_priority_missing_skills
        )

        recommendations.append(
            f"Medium-priority missing skills: {skills}. "
            "Consider highlighting relevant projects, coursework, "
            "or practical experience if you have it."
        )


    # --------------------------------------------------
    # Low Priority Missing Skills
    # --------------------------------------------------

    if low_priority_missing_skills:

        skills = ", ".join(
            low_priority_missing_skills
        )

        recommendations.append(
            f"Lower-priority missing skills: {skills}. "
            "These should generally receive less resume space than "
            "required skills."
        )


    # --------------------------------------------------
    # Technical Skills
    # --------------------------------------------------

    if technical_score < 60:

        recommendations.append(
            "Your technical skill coverage is relatively low. "
            "Review the technical requirements and make relevant "
            "technologies, tools, frameworks, databases, and platforms "
            "more visible where you have genuine experience."
        )

    elif technical_score < 80:

        recommendations.append(
            "Your technical skill coverage is moderate. "
            "Strengthen the most relevant technical skills by connecting "
            "them to projects or work experience."
        )

    else:

        recommendations.append(
            "Your technical skill coverage is strong. "
            "Keep technical skills focused on technologies relevant "
            "to the target role."
        )


    # --------------------------------------------------
    # Soft Skills
    # --------------------------------------------------

    if soft_skill_score < 60:

        recommendations.append(
            "Your resume has limited coverage of relevant soft skills. "
            "Where appropriate, demonstrate skills such as communication, "
            "leadership, teamwork, or problem-solving through concrete "
            "examples rather than only listing them."
        )

    elif soft_skill_score < 80:

        recommendations.append(
            "Your soft-skill coverage is moderate. "
            "Strengthen it by showing how you used interpersonal skills "
            "to achieve specific outcomes."
        )


    # --------------------------------------------------
    # Resume Quality
    # --------------------------------------------------

    if quality_score < 60:

        recommendations.append(
            "Your resume quality score indicates several areas need "
            "improvement. Review the quality warnings and strengthen "
            "the structure, content, and presentation."
        )

    elif quality_score < 80:

        recommendations.append(
            "Your resume quality is reasonable but can be improved. "
            "Address the quality warnings before applying."
        )

    else:

        recommendations.append(
            "Your resume structure and overall quality are strong. "
            "Continue keeping the document concise, targeted, and "
            "easy to scan."
        )


    # --------------------------------------------------
    # Word Count
    # --------------------------------------------------

    if word_count < 250:

        recommendations.append(
            "Your resume is quite short. "
            "Consider adding relevant project details, achievements, "
            "or experience if important information is missing."
        )

    elif word_count > 1000:

        recommendations.append(
            "Your resume is relatively long. "
            "Remove repetitive or low-value content and prioritize "
            "experience most relevant to the target role."
        )


    # --------------------------------------------------
    # Action Verbs
    # --------------------------------------------------

    if action_verb_count < 5:

        recommendations.append(
            "Use stronger action verbs in your experience and project "
            "descriptions, such as developed, implemented, optimized, "
            "designed, analyzed, automated, or delivered."
        )


    # --------------------------------------------------
    # Quantifiable Achievements
    # --------------------------------------------------

    if quantifiable_achievement_count < 3:

        recommendations.append(
            "Add more measurable achievements where possible. "
            "Use numbers such as percentages, revenue, time saved, "
            "users served, performance improvements, or project scale "
            "to demonstrate impact."
        )


    # --------------------------------------------------
    # Quality Warnings
    # --------------------------------------------------

    if quality_warnings:

        for warning in quality_warnings[:3]:

            recommendations.append(
                f"Address this resume quality issue: {warning}"
            )


    # --------------------------------------------------
    # Matching Skills
    # --------------------------------------------------

    if matching_skills:

        recommendations.append(
            "Your resume already contains relevant matching skills. "
            "Prioritize these skills in your summary, experience, "
            "and project descriptions where appropriate."
        )


    # --------------------------------------------------
    # Final Recommendation
    # --------------------------------------------------

    recommendations.append(
        "Before submitting the resume, tailor the most relevant "
        "experience and achievements to the specific job description "
        "while keeping all claims truthful and supported by your "
        "actual experience."
    )


    return recommendations