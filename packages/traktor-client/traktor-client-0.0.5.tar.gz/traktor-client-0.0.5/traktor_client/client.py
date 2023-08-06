from typing import Optional, List

from tea_client.client import TeaClient
from tea_client.handler import handler

from traktor_client.models import (
    Project,
    ProjectCreateRequest,
    ProjectUpdateRequest,
    Task,
    TaskCreateRequest,
    TaskUpdateRequest,
    Timer,
    Report,
)


class TraktorClient(TeaClient):
    # Projects

    @handler
    def project_list(self) -> List[Project]:
        return [Project(**p) for p in self.http.get("/projects/")]

    @handler
    def project_get(self, project_id: str) -> Project:
        return Project(**self.http.get(f"/projects/{project_id}/"))

    @handler
    def project_create(self, name: str, color: str = "#000000") -> Project:
        return Project(
            **self.http.post(
                "/projects/", data=ProjectCreateRequest(name=name, color=color)
            )
        )

    @handler
    def project_update(
        self,
        project_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
    ) -> Project:
        return Project(
            **self.http.patch(
                f"/projects/{project_id}/",
                data=ProjectUpdateRequest(name=name, color=color),
            )
        )

    @handler
    def project_delete(self, project_id: str):
        return self.http.delete(f"/projects/{project_id}/")

    # Tasks

    @handler
    def task_list(self, project_id: str) -> List[Task]:
        return [
            Task(**t) for t in self.http.get(f"/projects/{project_id}/tasks/")
        ]

    @handler
    def task_get(self, project_id: str, task_id: str) -> Task:
        return Task(
            **self.http.get(f"/projects/{project_id}/tasks/{task_id}/")
        )

    @handler
    def task_create(
        self, project_id: str, name: str, color: str = "#000000", default=False
    ) -> Task:

        return Task(
            **self.http.post(
                f"/projects/{project_id}/tasks/",
                data=TaskCreateRequest(
                    name=name, color=color, default=default
                ),
            )
        )

    @handler
    def task_update(
        self,
        project_id: str,
        task_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
        default: Optional[bool] = None,
    ) -> Task:

        return Task(
            **self.http.patch(
                f"/projects/{project_id}/tasks/{task_id}/",
                data=TaskUpdateRequest(
                    name=name, color=color, default=default
                ),
            )
        )

    @handler
    def task_delete(self, project_id: str, task_id: str):
        return self.http.delete(f"/projects/{project_id}/tasks/{task_id}/")

    # Timer

    @handler
    def timer_start(
        self, project_id: str, task_id: Optional[str] = None
    ) -> Timer:
        url = (
            f"/timer/start/{project_id}/"
            if task_id is None
            else f"/timer/start/{project_id}/{task_id}/"
        )
        return Timer(**self.http.post(url))

    @handler
    def timer_stop(self) -> Timer:
        return Timer(**self.http.post("/timer/stop/"))

    @handler
    def timer_status(self) -> Timer:
        return Timer(**self.http.get("/timer/status/"))

    @handler
    def timer_today(self) -> List[Report]:
        return [Report(**r) for r in self.http.get("/timer/today/")]

    @handler
    def timer_report(self, days: int = 0) -> List[Report]:
        return [
            Report(**r)
            for r in self.http.get(
                "/timer/report/", params={"days": str(days)}
            )
        ]
