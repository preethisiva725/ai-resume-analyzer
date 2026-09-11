from app.services.document_parser import extract_text
from app.services.skill_extractor import extract_skills
from app.services.matcher import compare_skills


# Resume
resume_file = r"C:\Users\Admin\ai-resume-analyzer\backend\uploads\Preethi_S_Resume.pdf"

resume_text = extract_text(resume_file)

resume_skills = extract_skills(resume_text)


# Job description
job_description = """
We are looking for a Python developer.

Required skills:
Python
FastAPI
SQL
Git
Docker
GitHub

The candidate should also understand object-oriented programming.
"""

job_skills = extract_skills(job_description)


# Compare resume and job description
result = compare_skills(resume_skills, job_skills)


print("Resume skills:")
print(resume_skills)

print()

print("Job description skills:")
print(job_skills)

print()

print("Matching skills:")
print(result["matching_skills"])

print()

print("Missing skills:")
print(result["missing_skills"])

print()

print("Match score:")
print(f'{result["match_score"]}%')