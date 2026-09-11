import re


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


def normalize_text(
    text: str
) -> str:

    return re.sub(
        r"\s+",
        " ",
        text.lower().strip()
    )


def contains_skill(
    text: str,
    skill: str
) -> bool:

    pattern = (
        r"(?<!\w)"
        + re.escape(
            skill.lower()
        )
        + r"(?!\w)"
    )

    return re.search(
        pattern,
        text,
        re.IGNORECASE
    ) is not None


def detect_priority_from_text(
    text: str
) -> str:

    text_lower = normalize_text(
        text
    )

    for keyword in REQUIRED_KEYWORDS:

        if keyword in text_lower:
            return "required"

    for keyword in PREFERRED_KEYWORDS:

        if keyword in text_lower:
            return "preferred"

    return "general"


def split_into_sections(
    job_description: str
) -> list[tuple[str, str]]:

    if not job_description:
        return []

    lines = job_description.splitlines()

    sections = []

    current_priority = "general"

    current_text = []

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            continue

        detected_priority = detect_priority_from_text(
            line
        )

        has_required_keyword = any(
            keyword in line.lower()
            for keyword in REQUIRED_KEYWORDS
        )

        has_preferred_keyword = any(
            keyword in line.lower()
            for keyword in PREFERRED_KEYWORDS
        )

        if has_required_keyword:

            current_priority = "required"

        elif has_preferred_keyword:

            current_priority = "preferred"

        current_text.append(
            line
        )

        sections.append(
            (
                current_priority,
                line
            )
        )

    return sections


def split_sentences(
    text: str
) -> list[str]:

    parts = re.split(
        r"(?<=[.!?;])\s+",
        text
    )

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


def detect_skill_priority(
    job_description: str,
    skill: str
) -> str:

    if not job_description or not skill:
        return "general"

    skill_lower = skill.lower()

    lines = [
        line.strip()
        for line in job_description.splitlines()
        if line.strip()
    ]

    # --------------------------------------------------
    # First check individual lines.
    # --------------------------------------------------

    for line in lines:

        if not contains_skill(
            line,
            skill_lower
        ):
            continue

        priority = detect_priority_from_text(
            line
        )

        if priority != "general":
            return priority

    # --------------------------------------------------
    # Check individual sentences.
    # This handles descriptions written as one paragraph.
    # --------------------------------------------------

    sentences = split_sentences(
        job_description
    )

    for sentence in sentences:

        if not contains_skill(
            sentence,
            skill_lower
        ):
            continue

        priority = detect_priority_from_text(
            sentence
        )

        if priority != "general":
            return priority

    # --------------------------------------------------
    # Handle section-style descriptions.
    #
    # Example:
    #
    # Required Skills:
    # Python
    # FastAPI
    # PostgreSQL
    #
    # Preferred:
    # Docker
    # AWS
    # --------------------------------------------------

    current_priority = "general"

    for line in lines:

        line_lower = line.lower()

        has_required_keyword = any(
            keyword in line_lower
            for keyword in REQUIRED_KEYWORDS
        )

        has_preferred_keyword = any(
            keyword in line_lower
            for keyword in PREFERRED_KEYWORDS
        )

        if has_required_keyword:

            current_priority = "required"

        elif has_preferred_keyword:

            current_priority = "preferred"

        if contains_skill(
            line,
            skill_lower
        ):

            return current_priority

    return "general"


def classify_job_skills(
    job_skills: list[str],
    job_description: str
) -> dict:

    result = {
        "required": [],
        "preferred": [],
        "general": []
    }

    if not job_skills:
        return result

    for skill in job_skills:

        priority = detect_skill_priority(
            job_description,
            skill
        )

        result[priority].append(
            skill
        )

    for category in result:

        result[category] = sorted(
            set(
                result[category]
            )
        )

    return result