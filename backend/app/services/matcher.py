import re


SKILL_WEIGHTS = {
    # Programming Languages
    "python": 3.0,
    "java": 3.0,
    "javascript": 2.5,
    "typescript": 2.5,
    "c": 2.0,
    "c++": 2.5,
    "c#": 2.5,
    "go": 2.5,
    "rust": 2.5,
    "php": 2.0,
    "ruby": 2.0,
    "kotlin": 2.0,
    "swift": 2.0,

    # Frontend
    "react": 2.5,
    "angular": 2.5,
    "vue": 2.5,
    "nextjs": 2.5,
    "bootstrap": 1.5,
    "tailwind": 1.5,

    # Backend
    "fastapi": 3.0,
    "django": 2.5,
    "flask": 2.5,
    "nodejs": 2.5,
    "express": 2.5,
    "spring": 2.5,
    "spring boot": 3.0,
    "asp.net": 2.5,

    # APIs
    "rest api": 2.0,
    "graphql": 2.0,
    "microservices": 2.5,

    # Databases
    "sql": 2.0,
    "mysql": 2.0,
    "postgresql": 2.5,
    "sqlite": 1.5,
    "mongodb": 2.0,
    "redis": 2.0,
    "oracle": 2.0,
    "sql server": 2.0,
    "firebase": 1.5,

    # Data / AI
    "pandas": 2.0,
    "numpy": 2.0,
    "matplotlib": 1.5,
    "scikit-learn": 2.5,
    "tensorflow": 3.0,
    "pytorch": 3.0,
    "machine learning": 3.0,
    "deep learning": 3.0,
    "ai": 2.5,
    "nlp": 2.5,
    "computer vision": 2.5,
    "genai": 3.0,
    "llm": 3.0,

    # Cloud
    "aws": 2.5,
    "azure": 2.5,
    "gcp": 2.5,

    # DevOps
    "docker": 2.5,
    "kubernetes": 3.0,
    "jenkins": 2.0,
    "terraform": 2.5,
    "ansible": 2.0,
    "linux": 1.5,
    "nginx": 1.5,

    # Version Control
    "git": 1.5,
    "github": 1.0,
    "gitlab": 1.0,
    "bitbucket": 1.0,

    # Engineering
    "oop": 2.0,
    "data structures": 2.5,
    "algorithms": 2.5,
    "system design": 3.0,
    "software development": 2.0,
    "software engineering": 2.0,
    "unit testing": 1.5,
    "testing": 1.5,
    "debugging": 1.5,
    "agile": 1.0,
    "scrum": 1.0,

    # Soft Skills
    "communication": 1.0,
    "written communication": 1.0,
    "verbal communication": 1.0,
    "teamwork": 1.0,
    "collaboration": 1.0,
    "leadership": 1.5,
    "problem solving": 1.5,
    "critical thinking": 1.5,
    "analytical thinking": 1.5,
    "time management": 1.0,
    "adaptability": 1.0,
    "flexibility": 1.0,
    "creativity": 1.0,
    "attention to detail": 1.0,
    "decision making": 1.0,
    "interpersonal skills": 1.0,
    "presentation skills": 1.0,
    "project management": 1.5,
    "mentoring": 1.0,
    "negotiation": 1.0,
}


REQUIRED_KEYWORDS = [
    "required",
    "must have",
    "must-have",
    "mandatory",
    "essential",
    "required skills",
    "requirements",
    "minimum qualifications",
]


PREFERRED_KEYWORDS = [
    "preferred",
    "preferred skills",
    "nice to have",
    "nice-to-have",
    "bonus",
    "desired",
    "plus",
    "good to have",
    "optional",
]


def get_skill_weight(
    skill: str
) -> float:

    return SKILL_WEIGHTS.get(
        skill.lower(),
        1.0
    )


def calculate_score(
    matching_skills: list[str],
    job_skills: list[str]
) -> float:

    if not job_skills:
        return 0.0

    matching_weight = sum(
        get_skill_weight(skill)
        for skill in matching_skills
    )

    total_weight = sum(
        get_skill_weight(skill)
        for skill in job_skills
    )

    if total_weight == 0:
        return 0.0

    return round(
        (matching_weight / total_weight) * 100,
        2
    )


def compare_skill_category(
    resume_skills: list[str],
    job_skills: list[str]
) -> dict:

    resume_set = set(
        resume_skills
    )

    job_set = set(
        job_skills
    )

    matching_skills = sorted(
        resume_set & job_set
    )

    missing_skills = sorted(
        job_set - resume_set
    )

    score = calculate_score(
        matching_skills,
        job_skills
    )

    return {
        "matching_skills":
            matching_skills,

        "missing_skills":
            missing_skills,

        "score":
            score
    }


def detect_skill_priority(
    job_description: str,
    skill: str
) -> str:

    text = job_description.lower()

    skill_lower = skill.lower()

    skill_pattern = re.escape(
        skill_lower
    )

    required_pattern = (
        r"("
        + "|".join(
            re.escape(keyword)
            for keyword in REQUIRED_KEYWORDS
        )
        + r").{0,120}"
        + skill_pattern
    )

    preferred_pattern = (
        r"("
        + "|".join(
            re.escape(keyword)
            for keyword in PREFERRED_KEYWORDS
        )
        + r").{0,120}"
        + skill_pattern
    )

    if re.search(
        required_pattern,
        text,
        re.IGNORECASE
    ):
        return "required"

    if re.search(
        preferred_pattern,
        text,
        re.IGNORECASE
    ):
        return "preferred"

    return "general"


def get_priority_weight(
    skill: str,
    priority: str
) -> float:

    base_weight = get_skill_weight(
        skill
    )

    if priority == "required":
        return base_weight * 1.5

    if priority == "preferred":
        return base_weight * 0.75

    return base_weight


def calculate_priority_score(
    matching_skills: list[str],
    job_skills: list[str],
    job_description: str
) -> float:

    if not job_skills:
        return 0.0

    matching_weight = 0.0

    total_weight = 0.0

    for skill in job_skills:

        priority = detect_skill_priority(
            job_description,
            skill
        )

        weight = get_priority_weight(
            skill,
            priority
        )

        total_weight += weight

        if skill in matching_skills:
            matching_weight += weight

    if total_weight == 0:
        return 0.0

    return round(
        (
            matching_weight /
            total_weight
        ) * 100,
        2
    )


def compare_skills(
    resume_skills: list[str],
    job_skills: list[str],
    resume_technical_skills: list[str] | None = None,
    job_technical_skills: list[str] | None = None,
    resume_soft_skills: list[str] | None = None,
    job_soft_skills: list[str] | None = None,
    job_description: str = ""
) -> dict:

    technical_result = compare_skill_category(
        resume_technical_skills or [],
        job_technical_skills or []
    )

    soft_result = compare_skill_category(
        resume_soft_skills or [],
        job_soft_skills or []
    )

    overall_result = compare_skill_category(
        resume_skills,
        job_skills
    )

    priority_score = calculate_priority_score(
        overall_result["matching_skills"],
        job_skills,
        job_description
    )

    return {
        "matching_skills":
            overall_result["matching_skills"],

        "missing_skills":
            overall_result["missing_skills"],

        "match_score":
            priority_score,

        "technical_matching_skills":
            technical_result["matching_skills"],

        "technical_missing_skills":
            technical_result["missing_skills"],

        "technical_score":
            technical_result["score"],

        "soft_matching_skills":
            soft_result["matching_skills"],

        "soft_missing_skills":
            soft_result["missing_skills"],

        "soft_score":
            soft_result["score"]
    }