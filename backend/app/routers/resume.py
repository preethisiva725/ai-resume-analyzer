from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException

from ..services.document_parser import extract_text


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    UPLOAD_DIR.mkdir(exist_ok=True)

    file_path = UPLOAD_DIR / file.filename

    file_content = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(file_content)

    try:
        extracted_text = extract_text(str(file_path))
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Could not extract text from resume: {error}"
        )

    return {
        "message": "Resume uploaded successfully.",
        "filename": file.filename,
        "text": extracted_text
    }