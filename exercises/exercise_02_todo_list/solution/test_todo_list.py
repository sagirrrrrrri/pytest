"""练习 2 参考答案：完整测试"""
import pytest

from todo_list import TodoList


@pytest.fixture
def todo(tmp_path):
    return TodoList(tmp_path / "data.json")


# ---------- 添加与查看 ----------
def test_add_and_list(todo):
    todo.add("买菜")
    todo.add("写作业")
    assert todo.list_tasks() == ["买菜", "写作业"]


def test_add_empty_raises(todo):
    with pytest.raises(ValueError, match="不能为空"):
        todo.add("")
    with pytest.raises(ValueError, match="不能为空"):
        todo.add("   ")


# ---------- 去重 ----------
def test_add_duplicate(todo):
    todo.add("买菜")
    with pytest.raises(ValueError, match="已存在"):
        todo.add("买菜")
    assert todo.list_tasks() == ["买菜"]


# ---------- 删除 ----------
def test_remove(todo):
    todo.add("买菜")
    todo.remove("买菜")
    assert todo.list_tasks() == []


def test_remove_missing_raises(todo):
    with pytest.raises(KeyError, match="不存在"):
        todo.remove("不存在的")


# ---------- 完成 ----------
def test_complete_moves_to_completed(todo):
    todo.add("写作业")
    todo.complete("写作业")
    assert todo.list_tasks() == []
    assert todo.completed_tasks() == ["写作业"]


def test_complete_missing_raises(todo):
    with pytest.raises(KeyError, match="不存在"):
        todo.complete("不存在")


# ---------- 持久化 ----------
def test_save_and_load_persistence(tmp_path):
    path = tmp_path / "data.json"
    todo1 = TodoList(path)
    todo1.add("买菜")
    todo1.add("写作业")
    todo1.save()

    todo2 = TodoList(path)   # 同一文件，新实例自动 load
    assert todo2.list_tasks() == ["买菜", "写作业"]


def test_save_after_complete(tmp_path):
    path = tmp_path / "data.json"
    todo1 = TodoList(path)
    todo1.add("写作业")
    todo1.complete("写作业")
    todo1.save()

    todo2 = TodoList(path)
    assert todo2.list_tasks() == []
    assert todo2.completed_tasks() == ["写作业"]
