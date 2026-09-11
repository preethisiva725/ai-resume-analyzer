import re


ACTION_VERBS = [
    "developed",
    "designed",
    "implemented",
    "created",
    "built",
    "managed",
    "led",
    "improved",
    "optimized",
    "automated",
    "analyzed",
    "configured",
    "deployed",
    "maintained",
    "tested",
    "integrated",
    "engineered",
    "delivered",
]


WEAK_PHRASES = [
    "hard worker",
    "hardworking",
    "team player",
    "go getter",
    "go-getter",
    "responsible for",
    "worked on",
    "helped with",
    "good communication",
    "excellent communication",
    "fast learner",
]


QUALITY_WEIGHTS = {
    "Contact Information": 10,
    "Education": 10,
    "Experience": 15,
    "Projects": 15,
    "Skills Section": 10,
    "Action Verbs": 10,
    "Quantifiable Achievements": 15,
    "Reasonable Length": 5,
    "LinkedIn": 5,
    "GitHub": 5,
}


def contains_pattern(
    text: str,
    pattern: str
) -> bool:
    """
    Check whether a regular expression pattern
    exists in the resume text.
    """

    return re.search(
        pattern,
        text,
        re.IGNORECASE
    ) is not None


def count_action_verbs(
    text: str
) -> int:
    """
    Count action verbs found in the resume.
    """

    text_lower = text.lower()

    count = 0

    for verb in ACTION_VERBS:

        pattern = (
            r"(?<!\w)"
            + re.escape(verb)
            + r"(?!\w)"
        )

        count += len(
            re.findall(
                pattern,
                text_lower
            )
        )

    return count


def count_quantifiable_achievements(
    text: str
) -> int:
    """
    Count lines containing numbers,
    percentages, money values, or measurable results.
    """

    lines = text.splitlines()

    count = 0

    for line in lines:

        if re.search(
            r"\d+%|\d+\+?|\$\d+",
            line
        ):

            count += 1

    return count


def analyze_resume_quality(
    text: str
) -> dict:
    """
    Analyze resume quality using weighted scoring.
    """

    if not text:

        return {
            "quality_score": 0,
            "checks": {},
            "strengths": [],
            "warnings": [],
            "word_count": 0,
            "action_verb_count": 0,
            "quantifiable_achievement_count": 0,
            "weak_phrases": [],
        }


    text_lower = text.lower()


    checks = {}

    strengths = []

    warnings = []


    # -----------------------------------------
    # CONTACT INFORMATION
    # -----------------------------------------

    has_email = contains_pattern(
        text,
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )


    has_phone = contains_pattern(
        text,
        r"(\+?\d[\d\s().-]{8,}\d)"
    )


    has_contact = (
        has_email and has_phone
    )


    checks["Contact Information"] = (
        has_contact
    )


    if has_contact:

        strengths.append(
            "Email address and phone number found."
        )

    elif has_email:

        strengths.append(
            "Email address found."
        )

        warnings.append(
            "Add a phone number."
        )

    elif has_phone:

        strengths.append(
            "Phone number found."
        )

        warnings.append(
            "Add a professional email address."
        )

    else:

        warnings.append(
            "Add professional contact information."
        )


    # -----------------------------------------
    # LINKEDIN
    # -----------------------------------------

    has_linkedin = (
        "linkedin.com"
        in text_lower
    )


    checks["LinkedIn"] = (
        has_linkedin
    )


    if has_linkedin:

        strengths.append(
            "LinkedIn profile detected."
        )

    else:

        warnings.append(
            "Consider adding your LinkedIn profile."
        )


    # -----------------------------------------
    # GITHUB
    # -----------------------------------------

    has_github = (
        "github.com"
        in text_lower
    )


    checks["GitHub"] = (
        has_github
    )


    if has_github:

        strengths.append(
            "GitHub profile detected."
        )

    else:

        warnings.append(
            "Consider adding a GitHub profile if relevant."
        )


    # -----------------------------------------
    # EDUCATION
    # -----------------------------------------

    education_keywords = [
        "education",
        "bachelor",
        "master",
        "b.tech",
        "m.tech",
        "degree",
        "university",
        "college",
    ]


    has_education = any(
        keyword in text_lower
        for keyword in education_keywords
    )


    checks["Education"] = (
        has_education
    )


    if has_education:

        strengths.append(
            "Education information detected."
        )

    else:

        warnings.append(
            "Add an education section."
        )


    # -----------------------------------------
    # EXPERIENCE
    # -----------------------------------------

    experience_keywords = [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internship",
        "intern",
        "developer",
        "engineer",
    ]


    has_experience = any(
        keyword in text_lower
        for keyword in experience_keywords
    )


    checks["Experience"] = (
        has_experience
    )


    if has_experience:

        strengths.append(
            "Professional experience information detected."
        )

    else:

        warnings.append(
            "Add relevant work experience or internships."
        )


    # -----------------------------------------
    # PROJECTS
    # -----------------------------------------

    project_keywords = [
        "projects",
        "project",
        "portfolio",
        "github repository",
    ]


    has_projects = any(
        keyword in text_lower
        for keyword in project_keywords
    )


    checks["Projects"] = (
        has_projects
    )


    if has_projects:

        strengths.append(
            "Project information detected."
        )

    else:

        warnings.append(
            "Add relevant projects to demonstrate practical skills."
        )


    # -----------------------------------------
    # SKILLS SECTION
    # -----------------------------------------

    skill_keywords = [
        "skills",
        "technical skills",
        "technologies",
        "technical expertise",
    ]


    has_skills_section = any(
        keyword in text_lower
        for keyword in skill_keywords
    )


    checks["Skills Section"] = (
        has_skills_section
    )


    if has_skills_section:

        strengths.append(
            "Skills section detected."
        )

    else:

        warnings.append(
            "Add a dedicated skills section."
        )


    # -----------------------------------------
    # ACTION VERBS
    # -----------------------------------------

    action_verb_count = count_action_verbs(
        text
    )


    has_action_verbs = (
        action_verb_count >= 3
    )


    checks["Action Verbs"] = (
        has_action_verbs
    )


    if has_action_verbs:

        strengths.append(
            f"Good use of action verbs ({action_verb_count} found)."
        )

    else:

        warnings.append(
            "Use stronger action verbs such as developed, "
            "implemented, designed, optimized, and automated."
        )


    # -----------------------------------------
    # QUANTIFIABLE ACHIEVEMENTS
    # -----------------------------------------

    achievement_count = (
        count_quantifiable_achievements(
            text
        )
    )


    has_achievements = (
        achievement_count >= 2
    )


    checks["Quantifiable Achievements"] = (
        has_achievements
    )


    if has_achievements:

        strengths.append(
            "Resume contains measurable achievements."
        )

    else:

        warnings.append(
            "Add measurable results such as percentages, "
            "numbers, time savings, or performance improvements."
        )


    # -----------------------------------------
    # WEAK PHRASES
    # -----------------------------------------

    found_weak_phrases = []


    for phrase in WEAK_PHRASES:

        if phrase in text_lower:

            found_weak_phrases.append(
                phrase
            )


    if found_weak_phrases:

        warnings.append(
            "Consider replacing weak phrases: "
            + ", ".join(
                found_weak_phrases
            )
        )

    else:

        strengths.append(
            "No common weak resume phrases detected."
        )


    # -----------------------------------------
    # RESUME LENGTH
    # -----------------------------------------

    word_count = len(
        re.findall(
            r"\b\w+\b",
            text
        )
    )


    has_reasonable_length = (
        150 <= word_count <= 1200
    )


    checks["Reasonable Length"] = (
        has_reasonable_length
    )


    if word_count < 150:

        warnings.append(
            "The resume appears very short. "
            "Add more relevant details."
        )

    elif word_count > 1200:

        warnings.append(
            "The resume may be too long. "
            "Consider removing less relevant information."
        )

    else:

        strengths.append(
            f"Resume length looks reasonable ({word_count} words)."
        )


    # -----------------------------------------
    # WEIGHTED SCORE
    # -----------------------------------------

    total_score = 0


    for check_name, weight in QUALITY_WEIGHTS.items():

        if checks.get(
            check_name,
            False
        ):

            total_score += weight


    quality_score = round(
        total_score,
        2
    )


    return {
        "quality_score":
            quality_score,

        "checks":
            checks,

        "strengths":
            strengths,

        "warnings":
            warnings,

        "word_count":
            word_count,

        "action_verb_count":
            action_verb_count,

        "quantifiable_achievement_count":
            achievement_count,

        "weak_phrases":
            found_weak_phrases,
    }