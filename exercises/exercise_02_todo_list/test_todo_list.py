"""练习 2 的测试骨架：先实现 todo_list.py，再补全这里的测试"""

import pytest

from todo_list import TodoList


@pytest.fixture
def todo(tmp_path):
    """每个测试独立的待办清单（临时存储文件）"""
    # TODO: 返回 TodoList(tmp_path / "data.json")
    return TodoList(tmp_path / "data.json")


# ---------- 添加与查看 ----------
def test_add_and_list(todo):
    # TODO: 添加两个任务，断言 list_tasks 返回 [..., ...]
    todo.add("第一个任务")
    todo.add("第二个任务")
    assert todo.tasks == ["第一个任务", "第二个任务"]


def test_add_empty_raises(todo):
    # TODO: add("") 与 add("   ") 抛 ValueError
    with pytest.raises(ValueError):
        todo.add("")
    with pytest.raises(ValueError):
        todo.add("   ")


# ---------- 去重 ----------
def test_add_duplicate(todo):
    # TODO: 添加两次"买菜"，断言 tasks 只有 1 条（或抛异常，二选一）
    todo.add("买菜")
    with pytest.raises(ValueError):
        todo.add("买菜")


# ---------- 删除 ----------
def test_remove(todo):
    # TODO: 添加后删除，断言 list_tasks 为空
    todo.add("待删除")
    todo.remove("待删除")
    assert todo.tasks == []


def test_remove_missing_raises(todo):
    # TODO: remove("不存在的") 抛 KeyError
    with pytest.raises(KeyError):
        todo.remove("不存在的")


# ---------- 完成 ----------
def test_complete_moves_to_completed(todo):
    # TODO: 添加"写作业"并 complete，断言已完成列表包含它、未完成列表为空
    todo.add("写作业")
    todo.complete("写作业")
    assert todo.tasks == []
    assert "写作业" in todo.completed


def test_complete_missing_raises(todo):
    # TODO: complete("不存在") 抛 KeyError
    with pytest.raises(KeyError):
        todo.complete("不存在")


# ---------- 持久化 ----------
def test_save_and_load_persistence(tmp_path):
    # TODO: 创建 todo1 添加任务并 save；再用同一路径创建 todo2 并 load
    # 断言 todo2 能看到 todo1 的任务
    path = tmp_path / "data.json"
    todo1 = TodoList(path)
    todo1.add("任务")
    todo1.save()
    todo2 = TodoList(path)
    assert todo2.tasks == todo1.tasks


def test_save_after_complete(tmp_path):
    # TODO: 添加+完成+save，新实例 load 后 completed 中保留该任务
    todo = TodoList(tmp_path / "data.json")
    todo.add("任务")
    todo.complete("任务")
    todo.save()
    todo2 = TodoList(tmp_path / "data.json")
    assert todo2.tasks == []
    assert "任务" in todo2.completed
