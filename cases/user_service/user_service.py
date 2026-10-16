"""
经典案例 5：用户服务（mock 外部依赖）
覆盖知识点：pytest-mock（mocker）、monkeypatch、模拟数据库/邮件、异常路径
运行方式：py312 -m pytest test_user_service.py -v
"""
import random
import time


class UserService:
    """用户服务：模拟"数据库查询 + 发邮件"的真实业务代码"""

    def __init__(self, db, notifier):
        self.db = db          # 数据库对象（有 fetch_user / save_user 方法）
        self.notifier = notifier  # 通知器（有 send_email 方法）

    def get_user_name(self, user_id: int) -> str:
        """从数据库取用户名"""
        user = self.db.fetch_user(user_id)
        if user is None:
            raise KeyError(f"用户不存在: {user_id}")
        return user["name"]

    def register(self, email: str, name: str) -> dict:
        """注册新用户：校验邮箱 → 存库 → 发欢迎邮件"""
        if "@" not in email:
            raise ValueError("邮箱格式不正确")
        user = {
            "id": random.randint(1000, 9999),
            "email": email,
            "name": name,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.db.save_user(user)
        self.notifier.send_email(email, "欢迎注册", f"你好，{name}！")
        return user

    def stats(self) -> dict:
        """返回服务运行状态"""
        return {
            "users_in_db": len(self.db.list_users()),
            "service_time": time.time(),
        }
