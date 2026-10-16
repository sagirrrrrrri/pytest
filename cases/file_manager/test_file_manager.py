"""经典案例 3 的测试：file_manager（重点演示 tmp_path fixture）"""
import pytest

from file_manager import FileManager


@pytest.fixture
def manager(tmp_path):
    """每个测试独立的临时目录管理器，测试结束自动清理"""
    return FileManager(tmp_path)


# ---------- 基础读写 ----------
def test_write_and_read_text(manager):
    manager.write_text("hello.txt", "你好，pytest！")
    assert manager.read_text("hello.txt") == "你好，pytest！"


def test_write_creates_subdirectory(manager):
    path = manager.write_text("sub/deep/data.txt", "x")
    assert path.exists()
    assert manager.read_text("sub/deep/data.txt") == "x"


# ---------- 异常路径 ----------
def test_read_missing_file_raises(manager):
    with pytest.raises(FileNotFoundError, match="不存在"):
        manager.read_text("no_such.txt")


# ---------- JSON 读写 ----------
def test_json_roundtrip(manager):
    data = {"name": "小明", "scores": [90, 85, 92]}
    manager.save_json("user.json", data)
    assert manager.load_json("user.json") == data


def test_json_preserves_chinese(manager):
    manager.save_json("note.json", {"内容": "中文测试"})
    raw = manager.read_text("note.json")
    assert "中文测试" in raw  # ensure_ascii=False 保证可读


# ---------- 列表与删除 ----------
def test_list_files(manager):
    manager.write_text("a.txt", "1")
    manager.write_text("b.txt", "2")
    assert sorted(manager.list_files()) == ["a.txt", "b.txt"]


def test_delete_existing_file(manager):
    manager.write_text("temp.txt", "delete me")
    assert manager.delete("temp.txt") is True
    assert "temp.txt" not in manager.list_files()


def test_delete_missing_file_returns_false(manager):
    assert manager.delete("ghost.txt") is False


# ---------- monkeypatch：模拟文件系统异常 ----------
def test_read_blocked_with_monkeypatch(manager, monkeypatch):
    """
    演示 monkeypatch 的经典用法：
    文件真实存在，但通过替换 Path.exists 模拟"文件突然消失"，
    验证 read_text 的异常分支 —— 不用真的删文件。
    用 monkeypatch.context() 限定替换的作用范围。
    """
    from pathlib import Path

    real_exists = Path.exists

    def fake_exists(self):
        if self.name == "blocked.txt":
            return False
        return real_exists(self)

    manager.write_text("blocked.txt", "内容")

    with monkeypatch.context() as m:
        m.setattr(Path, "exists", fake_exists)
        with pytest.raises(FileNotFoundError):
            manager.read_text("blocked.txt")
    # context 退出后替换已自动还原，读取恢复正常
    assert manager.read_text("blocked.txt") == "内容"


# ---------- tmp_path 隔离性演示 ----------
_seen_tmp_paths = []


def test_tmp_path_isolation_a(tmp_path):
    marker = tmp_path / "marker.txt"
    marker.write_text("A", encoding="utf-8")
    _seen_tmp_paths.append(tmp_path)
    assert marker.read_text(encoding="utf-8") == "A"


def test_tmp_path_isolation_b(tmp_path):
    marker = tmp_path / "marker.txt"
    assert not marker.exists()            # A 写入的文件不在这里
    assert tmp_path not in _seen_tmp_paths  # 目录与 A 完全不同
    marker.write_text("B", encoding="utf-8")
