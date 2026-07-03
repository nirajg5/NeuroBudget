"""
Goal Schemas
"""

from typing import Optional

from pydantic import BaseModel


class GoalBase(BaseModel):

    goal_name: str

    target_amount: float

    current_amount: float = 0

    deadline_months: int

    monthly_required: Optional[float] = None

    status: str = "Active"


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):

    goal_name: Optional[str] = None

    target_amount: Optional[float] = None

    current_amount: Optional[float] = None

    deadline_months: Optional[int] = None

    monthly_required: Optional[float] = None

    status: Optional[str] = None


class GoalResponse(GoalBase):

    goal_id: int

    class Config:

        from_attributes = True