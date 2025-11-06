import time
from models import Task, Artifact, TaskStatus
from typing import List, Dict, Optional

class StateManager:
    def __init__(self):
        self.task_backlog: Dict[str, Task] = {}
        self.artifact_store: Dict[str, Artifact] = {}

    def load_backlog(self, tasks: List[Task]):
        self.task_backlog = {task.id: task for task in tasks}

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.task_backlog.get(task_id)

    def update_task_status(self, task_id: str, status: TaskStatus, notes: str = ""):
        if task_id in self.task_backlog:
            self.task_backlog[task_id].status = status
            self.task_backlog[task_id].history.append({"status": status, "notes": notes, "time": time.time()})

    def add_artifact(self, artifact: Artifact):
        self.artifact_store[artifact.id] = artifact

    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        return self.artifact_store.get(artifact_id)

    def get_artifacts_for_task(self, task: Task) -> Dict[str, Artifact]:
        return {id: self.get_artifact(id) for id in task.inputs if self.get_artifact(id)}

    def get_next_task(self) -> Optional[Task]:
        for task in self.task_backlog.values():
            if task.status != TaskStatus.PENDING:
                continue
            deps_met = True
            for dep_id in task.deps:
                dep_task = self.get_task(dep_id)
                if not dep_task or dep_task.status != TaskStatus.PASSED_AUDIT:
                    deps_met = False
                    break
            if deps_met:
                return task
        return None