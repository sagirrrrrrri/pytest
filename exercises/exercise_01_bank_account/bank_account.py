"""练习 1：银行账户（实现我，然后写测试）"""

import pytest  # noqa: F401  （提示：测试里会用到）


class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self._balance = balance
        if self._balance < 0:
            raise ValueError("初始余额不能为负")

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("存款金额必须大于0")
        self._balance += amount          # 写余额：用私有属性 _balance
        return self._balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("取款金额必须大于0")
        elif self._balance < amount:
            raise ValueError("余额不足")
        self._balance -= amount          # 写余额：用私有属性 _balance
        return self._balance

    @property
    def balance(self) -> float:
        return self._balance

    def transfer_to(self, other: "BankAccount", amount: float) -> None:
        if amount <= 0:
            raise ValueError("转账金额必须大于0")
        if amount > self._balance:
            raise ValueError("转账余额不足")
        self._balance -= amount          # 写余额：用私有属性 _balance
        other._balance += amount         # 对方账户也是写私有属性
