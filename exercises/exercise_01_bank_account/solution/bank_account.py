"""练习 1 参考答案：bank_account 完整实现"""
import pytest  # noqa: F401


class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        if balance < 0:
            raise ValueError("初始余额不能为负")
        self.owner = owner
        self._balance = float(balance)

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("存款金额必须大于 0")
        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("取款金额必须大于 0")
        if amount > self._balance:
            raise ValueError("余额不足")
        self._balance -= amount
        return self._balance

    @property
    def balance(self) -> float:
        return self._balance

    def transfer_to(self, other: "BankAccount", amount: float) -> None:
        if amount <= 0:
            raise ValueError("转账金额必须大于 0")
        if amount > self._balance:
            raise ValueError("余额不足")
        # 全部校验通过后才变更状态
        self._balance -= amount
        other._balance += amount
