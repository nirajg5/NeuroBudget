"""
CRUD Operations for Financial Reports
"""

from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import Report

def create_report(
    db: Session,
    report: Report
) -> Report:

    db.add(report)

    db.commit()

    db.refresh(report)

    return report

def get_all_reports(
    db: Session
):

    return (
        db.query(Report)
        .order_by(
            Report.created_at.desc()
        )
        .all()
    )

def bulk_create_reports(
    db: Session,
    reports: List[Report]
):

    db.bulk_save_objects(reports)

    db.commit()

def get_report_by_id(
    db: Session,
    report_id: int
) -> Optional[Report]:

    return (
        db.query(Report)
        .filter(
            Report.report_id == report_id
        )
        .first()
    )

def get_report_by_id(
    db: Session,
    report_id: int
) -> Optional[Report]:

    return (
        db.query(Report)
        .filter(
            Report.report_id == report_id
        )
        .first()
    )

def get_latest_report(
    db: Session
):

    return (
        db.query(Report)
        .order_by(
            Report.created_at.desc()
        )
        .first()
    )

def get_latest_report(
    db: Session
):

    return (
        db.query(Report)
        .order_by(
            Report.created_at.desc()
        )
        .first()
    )

def update_report(
    db: Session,
    report_id: int,
    **kwargs
):

    report = get_report_by_id(
        db,
        report_id
    )

    if report is None:

        return None

    for key, value in kwargs.items():

        if hasattr(report, key):

            setattr(report, key, value)

    db.commit()

    db.refresh(report)

    return report

def delete_report(
    db: Session,
    report_id: int
):

    report = get_report_by_id(
        db,
        report_id
    )

    if report is None:

        return False

    db.delete(report)

    db.commit()

    return True

def delete_all_reports(
    db: Session
):

    db.query(Report).delete()

    db.commit()

def get_report_count(
    db: Session
):

    return (
        db.query(
            func.count(
                Report.report_id
            )
        )
        .scalar()
    )

def get_latest_pdf_path(
    db: Session
):

    report = get_latest_report(db)

    if report is None:

        return None

    return report.pdf_path

def get_latest_json_report(
    db: Session
):

    report = get_latest_report(db)

    if report is None:

        return None

    return report.report_json

def get_recent_reports(
    db: Session,
    limit: int = 10
):

    return (
        db.query(Report)
        .order_by(
            Report.created_at.desc()
        )
        .limit(limit)
        .all()
    )

def get_monthly_reports(
    db: Session
):

    return (
        db.query(Report)
        .filter(
            Report.report_type == "Monthly"
        )
        .all()
    )

def get_yearly_reports(
    db: Session
):

    return (
        db.query(Report)
        .filter(
            Report.report_type == "Yearly"
        )
        .all()
    )
