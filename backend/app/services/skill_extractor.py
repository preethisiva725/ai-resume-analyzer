import re


TECHNICAL_SKILLS = [
    # Programming Languages
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "go",
    "golang",
    "rust",
    "php",
    "ruby",
    "kotlin",
    "swift",
    "scala",
    "r",

    # Frontend
    "html",
    "css",
    "react",
    "react.js",
    "reactjs",
    "angular",
    "vue",
    "vue.js",
    "next.js",
    "nextjs",
    "bootstrap",
    "tailwind",
    "jquery",

    # Backend / APIs
    "node.js",
    "nodejs",
    "express",
    "express.js",
    "django",
    "flask",
    "fastapi",
    "spring",
    "spring boot",
    "asp.net",
    "rest api",
    "rest apis",
    "restful api",
    "graphql",
    "microservices",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "postgres",
    "sqlite",
    "mongodb",
    "redis",
    "oracle",
    "sql server",
    "mssql",
    "firebase",
    "dynamodb",

    # Data / AI / ML
    "pandas",
    "numpy",
    "matplotlib",
    "scikit-learn",
    "sklearn",
    "tensorflow",
    "pytorch",
    "keras",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai",
    "nlp",
    "natural language processing",
    "computer vision",
    "generative ai",
    "genai",
    "llm",
    "large language models",

    # Cloud / DevOps
    "aws",
    "amazon web services",
    "azure",
    "microsoft azure",
    "gcp",
    "google cloud",
    "google cloud platform",
    "docker",
    "kubernetes",
    "jenkins",
    "terraform",
    "ansible",
    "ci/cd",
    "continuous integration",
    "continuous deployment",
    "linux",
    "nginx",

    # Version Control / Tools
    "git",
    "github",
    "gitlab",
    "bitbucket",
    "jira",
    "postman",
    "vs code",
    "visual studio code",

    # Software Engineering
    "oop",
    "object oriented programming",
    "data structures",
    "algorithms",
    "system design",
    "software development",
    "software engineering",
    "unit testing",
    "testing",
    "debugging",
    "agile",
    "scrum",
]


SOFT_SKILLS = [
    "communication",
    "written communication",
    "verbal communication",
    "teamwork",
    "team player",
    "collaboration",
    "leadership",
    "problem solving",
    "problem-solving",
    "critical thinking",
    "analytical thinking",
    "time management",
    "adaptability",
    "flexibility",
    "creativity",
    "attention to detail",
    "decision making",
    "decision-making",
    "interpersonal skills",
    "presentation skills",
    "organization",
    "organization skills",
    "project management",
    "mentoring",
    "negotiation",
]


SKILL_ALIASES = {
    "react.js": "react",
    "reactjs": "react",

    "vue.js": "vue",

    "next.js": "nextjs",

    "node.js": "nodejs",

    "express.js": "express",

    "postgres": "postgresql",

    "sklearn": "scikit-learn",

    "golang": "go",

    "amazon web services": "aws",

    "microsoft azure": "azure",

    "google cloud": "gcp",

    "google cloud platform": "gcp",

    "artificial intelligence": "ai",

    "natural language processing": "nlp",

    "generative ai": "genai",

    "large language models": "llm",

    "object oriented programming": "oop",

    "rest apis": "rest api",

    "restful api": "rest api",

    "continuous integration": "ci/cd",

    "continuous deployment": "ci/cd",

    "problem-solving": "problem solving",

    "decision-making": "decision making",

    "team player": "teamwork",
}


def normalize_skill(
    skill: str
) -> str:

    normalized = skill.lower().strip()

    normalized = re.sub(
        r"\s+",
        " ",
        normalized
    )

    if normalized in SKILL_ALIASES:
        normalized = SKILL_ALIASES[
            normalized
        ]

    return normalized


def skill_pattern(
    skill: str
) -> str:

    escaped_skill = re.escape(
        skill
    )

    escaped_skill = escaped_skill.replace(
        r"\ ",
        r"\s+"
    )

    return (
        r"(?<!\w)"
        + escaped_skill
        + r"(?!\w)"
    )


def extract_from_list(
    text: str,
    skills: list[str]
) -> list[str]:

    if not text:
        return []

    found_skills = []

    for skill in skills:

        pattern = skill_pattern(
            skill
        )

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            normalized = normalize_skill(
                skill
            )

            if normalized not in found_skills:

                found_skills.append(
                    normalized
                )

    return sorted(
        found_skills
    )


def remove_redundant_skills(
    skills: list[str]
) -> list[str]:

    result = set(skills)

    if "rest api" in result:
        result.discard("api")

    return sorted(
        result
    )


def extract_skills(
    text: str
) -> list[str]:

    technical_skills = extract_technical_skills(
        text
    )

    soft_skills = extract_soft_skills(
        text
    )

    all_skills = (
        technical_skills +
        soft_skills
    )

    return remove_redundant_skills(
        sorted(
            set(all_skills)
        )
    )


def extract_technical_skills(
    text: str
) -> list[str]:

    skills = extract_from_list(
        text,
        TECHNICAL_SKILLS
    )

    return remove_redundant_skills(
        skills
    )


def extract_soft_skills(
    text: str
) -> list[str]:

    return extract_from_list(
        text,
        SOFT_SKILLS
    )