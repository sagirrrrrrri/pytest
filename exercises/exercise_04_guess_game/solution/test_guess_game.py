"""练习 4 参考答案：monkeypatch 完整测试"""
import pytest

from guess_game import guess_number


def _patch_answer(monkeypatch, answer):
    monkeypatch.setattr("guess_game.random.randint", lambda a, b: answer)


def _patch_inputs(monkeypatch, values):
    seq = iter(values)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(seq))


def test_guess_correct_first_try(monkeypatch):
    _patch_answer(monkeypatch, 42)
    _patch_inputs(monkeypatch, ["42"])
    result = guess_number()
    assert result == {"win": True, "attempts": 1, "answer": 42}


def test_guess_correct_after_several(monkeypatch):
    _patch_answer(monkeypatch, 42)
    _patch_inputs(monkeypatch, ["10", "50", "42"])
    result = guess_number()
    assert result["win"] is True
    assert result["attempts"] == 3
    assert result["answer"] == 42


def test_guess_fail_when_exhausted(monkeypatch):
    _patch_answer(monkeypatch, 42)
    _patch_inputs(monkeypatch, ["1", "2"])
    result = guess_number(max_attempts=2)
    assert result["win"] is False
    assert result["attempts"] == 2
    assert result["answer"] == 42


def test_invalid_input_not_counted(monkeypatch):
    _patch_answer(monkeypatch, 42)
    _patch_inputs(monkeypatch, ["abc", "xyz", "42"])
    result = guess_number()
    assert result["win"] is True
    assert result["attempts"] == 1   # 两次非法输入都不计次数


def test_answer_respects_range(monkeypatch):
    captured = {}
    def fake_randint(a, b):
        captured["range"] = (a, b)
        return 1
    monkeypatch.setattr("guess_game.random.randint", fake_randint)
    _patch_inputs(monkeypatch, ["1"])
    result = guess_number()
    assert result["win"] is True
    assert captured["range"] == (1, 100)


def test_custom_range(monkeypatch):
    _patch_answer(monkeypatch, 7)
    _patch_inputs(monkeypatch, ["7"])
    result = guess_number(low=1, high=10)
    assert result["win"] is True
    assert result["answer"] == 7
