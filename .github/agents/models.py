import time
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"
    FAILED_AUDIT = "FAILED_AUDIT"
    PASSED_AUDIT = "PASSED_AUDIT"

class Task(BaseModel):
    id: str = Field(..., description="Unique task identifier, e.g., TDS-ARCH-001")
    objective: str = Field(..., description="Concise action goal for the specialist")
    owner: str = Field(..., description="The specialist role ID, e.g., 'archon', 'coder'")
    deps: List[str] = Field(default_factory=list, description="List of Task IDs this task depends on")
    inputs: List[str] = Field(default_factory=list, description="List of artifact IDs needed as context")
    outputs: Dict[str, Any] = Field(..., description="Defines the expected output")
    acceptance: List[str] = Field(..., description="Acceptance criteria for the task")
    qualityGates: List[str] = Field(default_factory=list, description="List of Gate IDs to check")
    risk: str = Field(default="low", description="low|medium|high")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    history: List[Dict[str, Any]] = Field(default_factory=list, description="Log of status changes and reasons")

class Artifact(BaseModel):
    id: str = Field(..., description="Unique artifact identifier (often matches the task ID)")
    owner_task_id: str
    content: str
    format: str = Field(default="markdown", description="e.g., markdown, json, code, diagram")
    created_at: float = Field(default_factory=time.time)

class AuditResult(BaseModel):
    status: str = Field(..., description="PASS | FAIL")
    notes: str = Field(default="")