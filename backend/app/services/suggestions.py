def generate_suggestions(missing_skills: list[str]) -> list[str]:
    suggestions = []

    if not missing_skills:
        suggestions.append(
            "Your resume covers all the skills identified in the job description."
        )
        return suggestions

    for skill in missing_skills:
        suggestions.append(
            f"Consider adding {skill} to your resume if you have "
            f"experience with it."
        )

    suggestions.append(
        "Try to include specific projects, certifications, or practical "
        "experience related to the missing skills."
    )

    return suggestions