"""
Upload API
"""

from pathlib import Path
import shutil

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile
)
from sqlalchemy.orm import Session

from database.db import get_db
from service.upload_service import UploadService

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

UPLOAD_DIRECTORY = Path("uploads/raw")

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

@router.post("/csv")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

    file_path = UPLOAD_DIRECTORY / file.filename

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    service = UploadService(db)

    result = service.process_upload(file_path)

    return result