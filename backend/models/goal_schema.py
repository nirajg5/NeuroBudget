from pydantic import BaseModel, ConfigDict


class GoalBase(BaseModel):

    goal_name: str

    target_amount: float

    current_amount: float = 0

    deadline_months: int


class GoalCreate(GoalBase):

    pass


class GoalUpdate(BaseModel):

    current_amount: float


class GoalResponse(GoalBase):

    goal_id: int

    monthly_required: float | None = None

    status: str

    model_config = ConfigDict(from_attributes=True)