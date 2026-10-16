"""练习 2：待办清单（实现我，然后写测试）"""

import json
from pathlib import Path


class TodoList:
    def __init__(self, storage_path: Path):
        self.storage_path = Path(storage_path)
        self.tasks = []  # 未完成任务（有序）
        self.completed = []  # 已完成任务（有序）
        if self.storage_path.exists():
            self.load()

    def add(self, task: str) -> None:
        # TODO: 空字符串或纯空格抛 ValueError("任务不能为空")
        # TODO: 已存在的任务不要重复添加（抛 ValueError 或忽略，任选并保持一致）
        if not task.strip():
            raise ValueError("任务不能为空")
        if task in self.tasks:
            raise ValueError
        else:
            self.tasks += [task]

    def remove(self, task: str) -> None:
        # TODO: 任务不存在抛 KeyError(f"任务不存在: {task}")
        # TODO: 从 tasks 或 completed 中删除
        if task in self.tasks:
            self.tasks.remove(task)
        elif task in self.completed:
            self.completed.remove(task)
        else:
            raise KeyError(f"任务不存在: {task}")

    def list_tasks(self) -> list:
        return list(self.tasks)

    def complete(self, task: str) -> None:
        # TODO: 不存在抛 KeyError
        # TODO: 从 tasks 移到 completed
        if not task in self.tasks:
            raise KeyError(f"任务不存在: {task}")
        else:
            self.completed += [task]
            self.tasks.remove(task)

    def completed_tasks(self) -> list:
        return list(self.completed)

    ######这里不会！！！！！这里不会！！！！！这里不会！！！！！这里不会！！！！！######
    def save(self) -> None:
        # TODO: 写 JSON：{"tasks": [...], "completed": [...]}
        data = {"tasks": self.tasks, "completed": self.completed}
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.storage_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def load(self) -> None:
        # TODO: 读 JSON 并覆盖 tasks / completed
        data = json.loads(self.storage_path.read_text(encoding="utf-8"))
        self.tasks = data.get("tasks", [])
        self.completed = data.get("completed", [])
