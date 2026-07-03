"""
Goals APIs
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database.db import get_db
from database.models import Goal

from schemas.goal import (
    GoalCreate,
    GoalUpdate,
    GoalResponse
)

from database.crud.goal_crud import (
    create_goal,
    get_all_goals,
    get_goal_by_id,
    update_goal,
    delete_goal,
    get_active_goals,
    get_completed_goals,
    get_goal_count
)

router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)


# ==========================================================
# All Goals
# ==========================================================

@router.get(
    "",
    response_model=List[GoalResponse]
)
def read_goals(
    db: Session = Depends(get_db)
):
    return get_all_goals(db)


# ==========================================================
# Active Goals
# ==========================================================

@router.get(
    "/active",
    response_model=List[GoalResponse]
)
def active_goals(
    db: Session = Depends(get_db)
):
    return get_active_goals(db)


# ==========================================================
# Completed Goals
# ==========================================================

@router.get(
    "/completed",
    response_model=List[GoalResponse]
)
def completed_goals(
    db: Session = Depends(get_db)
):
    return get_completed_goals(db)


# ==========================================================
# Goal Count
# ==========================================================

@router.get("/count")
def goal_count(
    db: Session = Depends(get_db)
):
    return {
        "count": get_goal_count(db)
    }


# ==========================================================
# Goal By ID
# ==========================================================

@router.get(
    "/{goal_id}",
    response_model=GoalResponse
)
def read_goal(
    goal_id: int,
    db: Session = Depends(get_db)
):

    goal = get_goal_by_id(
        db,
        goal_id
    )

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    return goal


# ==========================================================
# Create Goal
# ==========================================================

@router.post(
    "",
    response_model=GoalResponse
)
def add_goal(
    goal: GoalCreate,
    db: Session = Depends(get_db)
):

    db_goal = Goal(**goal.model_dump())

    return create_goal(
        db,
        db_goal
    )


# ==========================================================
# Update Goal
# ==========================================================

@router.put(
    "/{goal_id}",
    response_model=GoalResponse
)
def edit_goal(
    goal_id: int,
    goal: GoalUpdate,
    db: Session = Depends(get_db)
):

    updated = update_goal(
        db,
        goal_id,
        **goal.model_dump(exclude_unset=True)
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    return updated


# ==========================================================
# Delete Goal
# ==========================================================

@router.delete("/{goal_id}")
def remove_goal(
    goal_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_goal(
        db,
        goal_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    return {
        "message": "Goal deleted successfully"
    }