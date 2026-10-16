# 练习 4：猜数字游戏（mock 随机数与输入）

> 难度：★★★☆☆ | 对应文档：第 3、5 章 | 预计 35 分钟

## 任务

实现一个猜数字游戏，并用 monkeypatch / mocker 让游戏**可复现、可测试**。

## 需求

```python
def guess_number(max_attempts: int = 5, low: int = 1, high: int = 100) -> dict:
    """游戏主逻辑（无 print，纯逻辑便于测试）：
    1. 随机生成答案（用 random.randint）
    2. 循环最多 max_attempts 次，每次从 input() 读取猜测
    3. 猜对 → 返回 {"win": True, "attempts": n, "answer": ans}
    4. 猜错且还有次数 → 继续
    5. 次数用尽 → 返回 {"win": False, "attempts": max_attempts, "answer": ans}
    6. 输入非数字 → 不计次数，提示重新输入（continue）
    """
```

## 要求

1. 用 `monkeypatch` 替换 `random.randint`，让答案固定（如 42）；
2. 用 `monkeypatch` 替换 `builtins.input`，提供预置的猜测序列；
3. 覆盖：一次猜中、多次猜中、次数用尽失败、非法输入不计次数；
4. 至少 6 个测试；
5. 返回值结构稳定（dict），方便断言。

## 运行方式

```powershell
cd "G:\QA2\pytest\exercises\exercise_04_guess_game"
py312 -m pytest test_guess_game.py -v
```

## 提示

- 替换内置函数：`monkeypatch.setattr("builtins.input", lambda _: "42")`；
- 替换模块内 random：`monkeypatch.setattr("guess_game.random.randint", lambda a, b: 42)`；
- 输入序列用迭代器：`iter(["10", "42"])`，`lambda _: next(seq)`；
- 测试非法输入：`iter(["abc", "42"])` → 应能最终猜中，且 attempts 只算 1 次（abc 不计）；
- 想挑战自己？再用 `mocker.patch` 写一遍相同测试，对比两种写法。

写完后对照 `solution/` 参考答案。
