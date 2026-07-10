from enum import Enum
from pydantic import BaseModel, Field


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class PlanStep(BaseModel):
    id: int
    description: str
    expected_output: str
    depends_on: list[int] = Field(default_factory=list)
    status: StepStatus = StepStatus.PENDING


class ExecutionPlan(BaseModel):
    goal: str
    summary: str
    steps: list[PlanStep]