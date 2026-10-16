"""练习 4 的测试骨架：先实现 guess_game.py，再用 monkeypatch 补全测试"""

import pytest
from guess_game import guess_number


# ---------- 一次猜中 ----------
def test_guess_correct_first_try(monkeypatch):
    # TODO: 固定答案 42，输入序列 ["42"]
    monkeypatch.setattr("random.randint", lambda a, b: 42)
    monkeypatch.setattr("builtins.input", lambda _: "42")
    # 断言返回 {"win": True, "attempts": 1, "answer": 42}
    assert guess_number() == {"win": True, "attempts": 1, "answer": 42}


# ---------- 多次后猜中 ----------
def test_guess_correct_after_several(monkeypatch):
    # TODO: 固定答案 42，输入 ["10", "50", "42"] → win=True, attempts=3
    inputs = iter(["10", "50", "42"])
    monkeypatch.setattr("random.randint", lambda a, b: 42)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert guess_number() == {"win": True, "attempts": 3, "answer": 42}


# ---------- 次数用尽失败 ----------
def test_guess_fail_when_exhausted(monkeypatch):
    # TODO: 固定答案 42，max_attempts=2，输入 ["1", "2"] → win=False, attempts=2
    inputs = iter(["1", "2"])
    monkeypatch.setattr("random.randint", lambda a, b: 42)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert guess_number(max_attempts=2) == {"win": False, "attempts": 2, "answer": 42}


# ---------- 非法输入不计次数 ----------
def test_invalid_input_not_counted(monkeypatch):
    # TODO: 固定答案 42，输入 ["abc", "xyz", "42"] → win=True, attempts=1
    inputs = iter(["abc", "xyz", "42"])
    monkeypatch.setattr("random.randint", lambda a, b: 42)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert guess_number() == {"win": True, "attempts": 1, "answer": 42}


# ---------- 输入区间边界 ----------
def test_answer_respects_range(monkeypatch):
    # TODO: 用 lambda 记录 randint 收到的参数：固定答案 1，输入 ["1"]
    monkeypatch.setattr("random.randint", lambda a, b: 1)
    monkeypatch.setattr("builtins.input", lambda _: "1")
    # 断言 win=True，且 randint 被调用的范围是 (1, 100) 或自定义范围
    assert guess_number(low=1, high=100)["win"] == True


# ---------- 自定义区间 ----------
def test_custom_range(monkeypatch):
    # TODO: low=1, high=10，固定答案 7，输入 ["7"] → win=True
    monkeypatch.setattr("random.randint", lambda a, b: 7)
    monkeypatch.setattr("builtins.input", lambda _: "7")
    assert guess_number(low=1, high=10)["win"] == True
