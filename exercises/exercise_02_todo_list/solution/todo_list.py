"""练习 2 参考答案：todo_list 完整实现"""
import json
from pathlib import Path


class TodoList:
    def __init__(self, storage_path: Path):
        self.storage_path = Path(storage_path)
        self.tasks = []
        self.completed = []
        if self.storage_path.exists():
            self.load()

    def add(self, task: str) -> None:
        if not task.strip():
            raise ValueError("任务不能为空")
        if task in self.tasks or task in self.completed:
            raise ValueError(f"任务已存在: {task}")
        self.tasks.append(task)

    def remove(self, task: str) -> None:
        if task in self.tasks:
            self.tasks.remove(task)
        elif task in self.completed:
            self.completed.remove(task)
        else:
            raise KeyError(f"任务不存在: {task}")

    def list_tasks(self) -> list:
        return list(self.tasks)

    def complete(self, task: str) -> None:
        if task not in self.tasks:
            raise KeyError(f"任务不存在: {task}")
        self.tasks.remove(task)
        self.completed.append(task)

    def completed_tasks(self) -> list:
        return list(self.completed)

    def save(self) -> None:
        data = {"tasks": self.tasks, "completed": self.completed}
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.storage_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def load(self) -> None:
        data = json.loads(self.storage_path.read_text(encoding="utf-8"))
        self.tasks = data.get("tasks", [])
        self.completed = data.get("completed", [])
