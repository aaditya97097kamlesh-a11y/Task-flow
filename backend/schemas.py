from pydantic import BaseModel, field_validator
from typing import Optional


# -------------------------
# Task
# -------------------------

class TaskCreate(BaseModel):
    title: str
    priority: str
    due_date: Optional[str] = None
    project_id: int

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be blank")
        return value

    @field_validator("priority")
    @classmethod
    def check_priority(cls, value):
        if value not in ["low", "medium", "high"]:
            raise ValueError("Priority must be low, medium or high")
        return value


class TaskResponse(BaseModel):
    id: int
    title: str
    priority: str
    due_date: Optional[str] = None
    project_id: int

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: str
    priority: str
    due_date: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be blank")
        return value

    @field_validator("priority")
    @classmethod
    def check_priority(cls, value):
        if value not in ["low", "medium", "high"]:
            raise ValueError("Priority must be low, medium or high")
        return value


# -------------------------
# User
# -------------------------

class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# -------------------------
# Project
# -------------------------

class ProjectCreate(BaseModel):
    name: str
    owner_id: int


class ProjectResponse(BaseModel):
    id: int
    name: str
    owner_id: int

    class Config:
        from_attributes = True