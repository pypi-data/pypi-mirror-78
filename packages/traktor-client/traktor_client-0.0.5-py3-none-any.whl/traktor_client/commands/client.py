from typing import Optional

import typer

from tea_console.console import command

from traktor_client.config import config
from traktor_client.client import TraktorClient


client = TraktorClient(config=config)


# Projects

project_app = typer.Typer(name="project", help="Project commands.")


@command(project_app, name="list")
def project_list():
    """List all projects."""
    return client.project_list()


@command(project_app, name="get")
def project_get(project_id: str):
    """Get a project."""
    return client.project_get(project_id=project_id)


@command(project_app, name="create")
def project_create(name: str, color: str = typer.Option("#000000")):
    """Create a project."""
    return client.project_create(name=name, color=color)


@command(project_app, name="update")
def project_update(
    project_id: str, name: Optional[str] = None, color: Optional[str] = None
):
    """Update a project."""
    return client.project_update(project_id=project_id, name=name, color=color)


@command(project_app, name="delete")
def project_delete(project_id: str):
    """Delete a project."""
    return client.project_delete(project_id=project_id)


# Tasks

task_app = typer.Typer(name="task", help="Task commands.")


@command(task_app, name="list")
def task_list(project_id: str):
    """List all tasks in a project."""
    return client.task_list(project_id=project_id)


@command(task_app, name="get")
def task_get(project_id: str, task_id: str):
    """Get a task."""
    return client.task_get(project_id=project_id, task_id=task_id)


@command(task_app, name="create")
def task_create(
    project_id: str,
    name: str,
    color: str = typer.Option("#000000"),
    default: bool = False,
):
    """Create a task."""
    return client.task_create(
        project_id=project_id, name=name, color=color, default=default
    )


@command(task_app, name="update")
def task_update(
    project_id: str,
    task_id: str,
    name: Optional[str] = None,
    color: Optional[str] = None,
    default: Optional[bool] = None,
):
    """Update a task."""
    return client.task_update(
        project_id=project_id,
        task_id=task_id,
        name=name,
        color=color,
        default=default,
    )


@command(task_app, name="delete")
def task_delete(project_id: str, task_id: str):
    """Delete a task."""
    return client.task_delete(project_id=project_id, task_id=task_id)


# Timer

timer_app = typer.Typer(name="timer", help="Timer commands.")


@command(timer_app, name="start")
def timer_start(project_id: str, task_id: Optional[str] = None):
    """Start timer."""
    return client.timer_start(project_id=project_id, task_id=task_id)


@command(timer_app, name="stop")
def timer_stop():
    """Stop timer."""
    return client.timer_stop()


@command(timer_app, name="status")
def timer_status():
    """Get timer status."""
    return client.timer_status()


@command(timer_app, name="today")
def timer_today():
    """Get report for today."""
    return client.timer_today()


@command(timer_app, name="report")
def timer_report(days: int = 0):
    """Get report for multiple days."""
    return client.timer_report(days=days)
