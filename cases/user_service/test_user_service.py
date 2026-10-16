"""经典案例 5 的测试：user_service（重点演示 mocker / monkeypatch）"""
import pytest

from user_service import UserService


@pytest.fixture
def fake_db():
    """假数据库：内存字典模拟"""
    class FakeDB:
        def __init__(self):
            self._users = {}

        def fetch_user(self, user_id):
            return self._users.get(user_id)

        def save_user(self, user):
            self._users[user["id"]] = user

        def list_users(self):
            return list(self._users.values())

    return FakeDB()


@pytest.fixture
def fake_notifier():
    """假通知器：记录发出的邮件"""
    class FakeNotifier:
        def __init__(self):
            self.sent = []

        def send_email(self, to, subject, body):
            self.sent.append((to, subject, body))

    return FakeNotifier()


@pytest.fixture
def service(fake_db, fake_notifier):
    return UserService(fake_db, fake_notifier)


# ---------- 使用假对象（替身） ----------
def test_get_user_name(service, fake_db):
    fake_db.save_user({"id": 1, "name": "小明"})
    assert service.get_user_name(1) == "小明"


def test_get_missing_user_raises(service):
    with pytest.raises(KeyError, match="用户不存在"):
        service.get_user_name(999)


# ---------- 使用 mocker 模拟数据库 ----------
def test_register_with_mocker(service, mocker):
    """mocker 替换 random.randint，保证结果可复现"""
    mocker.patch("user_service.random.randint", return_value=1000)

    user = service.register("xiao@example.com", "小明")

    assert user["id"] == 1000           # 被 mock 固定
    assert user["name"] == "小明"
    assert service.get_user_name(1000) == "小明"  # 已入库
    assert ("xiao@example.com", "欢迎注册", "你好，小明！") in service.notifier.sent


def test_register_invalid_email(service):
    with pytest.raises(ValueError, match="邮箱"):
        service.register("not-an-email", "小明")


def test_register_notifier_receives_email(service):
    service.register("a@b.com", "小玉")
    assert len(service.notifier.sent) == 1
    to, subject, body = service.notifier.sent[0]
    assert to == "a@b.com"
    assert subject == "欢迎注册"
    assert "小玉" in body


# ---------- monkeypatch 模拟时间 ----------
def test_stats_time_fixed(service, monkeypatch):
    """monkeypatch 固定 time.time，验证 stats 可复现"""
    monkeypatch.setattr("user_service.time.time", lambda: 1234567890.0)
    stats = service.stats()
    assert stats["service_time"] == pytest.approx(1234567890.0)


# ---------- 更彻底：直接替换整个依赖对象 ----------
def test_service_with_mocked_db(service, mocker):
    """演示 mocker.patch 替换实例方法"""
    mocker.patch.object(service.db, "fetch_user", return_value={"id": 9, "name": "完全mock"})
    assert service.get_user_name(9) == "完全mock"
    service.db.fetch_user.assert_called_once_with(9)


def test_side_effect_simulation(service, mocker):
    """side_effect：第一次返回用户，第二次抛异常（模拟数据库抖动）"""
    mocker.patch.object(
        service.db,
        "fetch_user",
        side_effect=[{"id": 1, "name": "小明"}, KeyError("数据库暂时不可用")],
    )
    assert service.get_user_name(1) == "小明"
    with pytest.raises(KeyError):
        service.get_user_name(1)
