"""
CRUD Operations for Financial Goals
"""

from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from database.models import Goal

def create_goal(
    db: Session,
    goal: Goal
) -> Goal:
    """
    Create a new financial goal.
    """

    db.add(goal)

    db.commit()

    db.refresh(goal)

    return goal


def get_goal_by_id(
    db: Session,
    goal_id: int
) -> Optional[Goal]:

    return (
        db.query(Goal)
        .filter(
            Goal.goal_id == goal_id
        )
        .first()
    )

def get_all_goals(
    db: Session
) -> List[Goal]:

    return (
        db.query(Goal)
        .order_by(
            Goal.created_at.desc()
        )
        .all()
    )

def update_goal(
    db: Session,
    goal_id: int,
    **kwargs
):

    goal = get_goal_by_id(
        db,
        goal_id
    )

    if goal is None:

        return None

    for key, value in kwargs.items():

        if hasattr(goal, key):

            setattr(goal, key, value)

    db.commit()

    db.refresh(goal)

    return goal

def delete_goal(
    db: Session,
    goal_id: int
):

    goal = get_goal_by_id(
        db,
        goal_id
    )

    if goal is None:

        return False

    db.delete(goal)

    db.commit()

    return True

def update_current_amount(
    db: Session,
    goal_id: int,
    amount: float
):

    goal = get_goal_by_id(
        db,
        goal_id
    )

    if goal is None:

        return None

    goal.current_amount = amount

    db.commit()

    db.refresh(goal)

    return goal

def get_goal_progress(
    db: Session,
    goal_id: int
):

    goal = get_goal_by_id(
        db,
        goal_id
    )

    if goal is None:

        return None

    progress = (
        goal.current_amount /
        goal.target_amount
    ) * 100

    return round(progress, 2)

def get_remaining_amount(
    db: Session,
    goal_id: int
):

    goal = get_goal_by_id(
        db,
        goal_id
    )

    if goal is None:

        return None

    return max(
        goal.target_amount -
        goal.current_amount,
        0
    )

def get_monthly_required(
    db: Session,
    goal_id: int
):

    goal = get_goal_by_id(
        db,
        goal_id
    )

    if goal is None:

        return None

    remaining = max(
        goal.target_amount -
        goal.current_amount,
        0
    )

    if goal.deadline_months == 0:

        return None

    return round(
        remaining / goal.deadline_months,
        2
    )

def get_active_goals(
    db: Session
):

    return (
        db.query(Goal)
        .filter(
            Goal.status == "Active"
        )
        .all()
    )

def get_completed_goals(
    db: Session
):

    return (
        db.query(Goal)
        .filter(
            Goal.status == "Completed"
        )
        .all()
    )

def get_goal_count(
    db: Session
):

    return (
        db.query(
            func.count(Goal.goal_id)
        )
        .scalar()
    )
def complete_goal(
    db: Session,
    goal_id: int
):

    goal = get_goal_by_id(
        db,
        goal_id
    )

    if goal is None:

        return None

    goal.status = "Completed"

    db.commit()

    db.refresh(goal)

    return goal

    