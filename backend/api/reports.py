"""
Reports APIs
"""

from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.db import get_db
from database.models import Report

from schemas.report import (
    ReportCreate,
    ReportUpdate,
    ReportResponse
)

from database.crud.report_crud import (
    create_report,
    get_all_reports,
    get_latest_report,
    get_monthly_reports,
    get_yearly_reports,
    get_report_by_id,
    update_report,
    delete_report,
    get_report_count,
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

# ==========================================================
# All Reports
# ==========================================================

@router.get(
    "",
    response_model=List[ReportResponse]
)
def read_reports(
    db: Session = Depends(get_db)
):

    return get_all_reports(db)


# ==========================================================
# Latest Report
# ==========================================================

@router.get(
    "/latest",
    response_model=ReportResponse
)
def latest_report(
    db: Session = Depends(get_db)
):

    report = get_latest_report(db)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="No report found"
        )

    return report


# ==========================================================
# Monthly Reports
# ==========================================================

@router.get(
    "/monthly",
    response_model=List[ReportResponse]
)
def monthly_reports(
    db: Session = Depends(get_db)
):

    return get_monthly_reports(db)


# ==========================================================
# Yearly Reports
# ==========================================================

@router.get(
    "/yearly",
    response_model=List[ReportResponse]
)
def yearly_reports(
    db: Session = Depends(get_db)
):

    return get_yearly_reports(db)


# ==========================================================
# Report Count
# ==========================================================

@router.get("/count")
def report_count(
    db: Session = Depends(get_db)
):

    return {
        "count": get_report_count(db)
    }


# ==========================================================
# Report By ID
# ==========================================================

@router.get(
    "/{report_id}",
    response_model=ReportResponse
)
def read_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = get_report_by_id(
        db,
        report_id
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return report


# ==========================================================
# Create Report
# ==========================================================

@router.post(
    "",
    response_model=ReportResponse
)
def add_report(
    report: ReportCreate,
    db: Session = Depends(get_db)
):

    db_report = Report(
        **report.model_dump()
    )

    return create_report(
        db,
        db_report
    )


# ==========================================================
# Update Report
# ==========================================================

@router.put(
    "/{report_id}",
    response_model=ReportResponse
)
def edit_report(
    report_id: int,
    report: ReportUpdate,
    db: Session = Depends(get_db)
):

    updated = update_report(
        db,
        report_id,
        **report.model_dump(
            exclude_unset=True
        )
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return updated


# ==========================================================
# Delete Report
# ==========================================================

@router.delete("/{report_id}")
def remove_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_report(
        db,
        report_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return {
        "message": "Report deleted successfully"
    }