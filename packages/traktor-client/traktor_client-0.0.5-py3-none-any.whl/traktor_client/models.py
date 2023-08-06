from datetime import datetime
from typing import Optional

from tea_client.models import TeaClientModel, ColoredModel, ColoredUpdateModel


# Project


class Project(ColoredModel):
    id: str
    user: str
    name: str
    color: str
    created_on: datetime
    updated_on: datetime


class ProjectCreateRequest(ColoredModel):
    name: str


class ProjectUpdateRequest(ColoredUpdateModel):
    name: Optional[str] = None


# Task


class Task(ColoredModel):
    user: str
    project: str
    id: str
    name: str
    default: bool
    created_on: datetime
    updated_on: datetime


class TaskCreateRequest(ColoredModel):
    name: str
    default: bool


class TaskUpdateRequest(ColoredUpdateModel):
    name: Optional[str] = None
    default: Optional[bool] = None


class Timer(TeaClientModel):
    user: str
    project: str
    task: str
    description: str
    notes: str
    running_time: str
    created_on: datetime
    updated_on: datetime
    start_time: datetime
    duration: int
    end_time: Optional[datetime] = None


class Report(TeaClientModel):
    user: str
    project: str
    task: str
    duration: int
    running_time: str
