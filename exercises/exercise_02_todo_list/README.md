# 练习 2：待办清单（fixture 与 tmp_path）

> 难度：★★☆☆☆ | 对应文档：第 3 章 | 预计 30 分钟

## 任务

实现一个带**文件持久化**的待办清单 `TodoList`，并用 fixture + tmp_path 编写测试。

## 需求

```python
class TodoList:
    def __init__(self, storage_path: Path):
        """storage_path: JSON 文件路径；文件不存在则从空清单开始"""

    def add(self, task: str) -> None:
        """添加任务；空字符串抛 ValueError"""

    def remove(self, task: str) -> None:
        """删除任务；不存在抛 KeyError"""

    def list_tasks(self) -> list:
        """返回任务列表（保持添加顺序）"""

    def complete(self, task: str) -> None:
        """标记任务完成；不存在抛 KeyError"""

    def completed_tasks(self) -> list:
        """返回已完成任务列表"""

    def save(self) -> None:
        """把当前状态写入 JSON 文件"""

    def load(self) -> None:
        """从 JSON 文件读取状态（覆盖内存中的当前状态）"""
```

## 要求

1. 用 `tmp_path` 让每个测试使用独立的存储文件；
2. 用一个 fixture 统一创建"带临时文件的 TodoList"，测试函数通过参数注入；
3. 覆盖：添加、去重、删除、完成、持久化（save → load 后数据仍在）；
4. 异常路径：空任务、删除不存在的任务；
5. 至少 8 个测试。

## 运行方式

```powershell
cd "G:\QA2\pytest\exercises\exercise_02_todo_list"
py312 -m pytest test_todo_list.py -v
```

## 提示

- 持久化格式建议：`{"tasks": [...], "completed": [...]}`；
- fixture 返回的对象里已经包含 `tmp_path / "data.json"` 的路径；
- 测试"持久化"：`add("买菜") → save() → 新建一个 TodoList 指向同一文件 → load() → 断言任务还在`；
- 验证隔离：两个测试写入同名文件互不干扰（这正是 tmp_path 的价值）。

写完后对照 `solution/` 参考答案。
