# 练习 1：银行账户（基础断言与异常）

> 难度：★☆☆☆☆ | 对应文档：第 2 章 | 预计 20 分钟

## 任务

实现一个 `BankAccount` 类，并用 pytest 为它编写测试。

## 需求

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        """开户：owner 姓名，初始余额 balance（不得为负）"""

    def deposit(self, amount: float) -> float:
        """存款：返回新余额；amount 必须 > 0，否则抛 ValueError"""

    def withdraw(self, amount: float) -> float:
        """取款：返回新余额；amount 必须 > 0 且不超过余额，否则抛 ValueError"""

    @property
    def balance(self) -> float:
        """当前余额"""

    def transfer_to(self, other: "BankAccount", amount: float) -> None:
        """转账：从本账户扣款到 other 账户；余额不足抛 ValueError"""
```

## 要求

1. 先想清楚每个方法的**输入、输出、异常**，再写测试；
2. 用 `pytest.raises` 覆盖异常路径；
3. 浮点数比较用 `pytest.approx`；
4. 至少 8 个测试函数。

## 运行方式

```powershell
cd "G:\QA2\pytest\exercises\exercise_01_bank_account"
py312 -m pytest test_bank_account.py -v
```

## 提示

- 账户初始余额为负 → `__init__` 里抛 `ValueError`；
- 取款超过余额 → 抛 `ValueError` 且**余额不变**；
- 转账失败时，**两个账户余额都不变**（先校验再扣款）；
- 写测试时注意：每个测试用独立账户实例，避免互相影响。

写完后可对照 `solution/` 中的参考答案。
