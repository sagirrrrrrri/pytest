"""练习 1 的测试骨架：先实现 bank_account.py，再补全这里的测试"""

# py312 -m pytest test_bank_account.py -v
import pytest

from bank_account import BankAccount


# ---------- 开户 ----------
def test_create_account():
    account = BankAccount("小明", 100.0)
    assert account.owner == "小明"
    assert account.balance == pytest.approx(100.0)


def test_default_balance_is_zero():
    account = BankAccount("小玉")
    assert account.balance == 0


def test_negative_initial_balance_raises():
    with pytest.raises(ValueError, match="不能为负"):
        BankAccount("小红", -50.0)


# ---------- 存款 ----------
def test_deposit():
    # TODO: 开户 100，存 50，断言余额 150 且返回 150
    account = BankAccount("乐爷", 100.0)
    account.deposit(50.0)
    assert account.balance == pytest.approx(150.0)


def test_deposit_zero_raises():
    # TODO: 存 0 抛 ValueError
    account = BankAccount("乐子乐", 100)
    with pytest.raises(ValueError) as exc_info:
        account.deposit(0)
    assert "存款金额必须大于0" in str(exc_info.value)


def test_deposit_negative_raises():
    # TODO: 存 -10 抛 ValueError
    account = BankAccount("小红", 100)
    with pytest.raises(ValueError) as exc_info:
        account.deposit(-10)
    assert "存款金额必须大于0" in str(exc_info.value)


# ---------- 取款 ----------
def test_withdraw():
    # TODO: 开户 100，取 30，断言余额 70
    account = BankAccount("小兰", 100)
    assert account.withdraw(30) == pytest.approx(70)


def test_withdraw_over_balance_raises():
    # TODO: 开户 100，取 150 抛 ValueError
    # 并且余额仍为 100（失败后状态不变）
    account = BankAccount("小绿", 100)
    with pytest.raises(ValueError) as exc_info:
        account.withdraw(150)
    assert "余额不足" in str(exc_info.value)


def test_withdraw_zero_raises():
    # TODO: 取 0 抛 ValueError
    account = BankAccount("小灰", 100)
    with pytest.raises(ValueError) as exc_info:
        account.withdraw(0)
    assert "取款金额必须大于0" in str(exc_info.value)


# ---------- 转账 ----------
def test_transfer():
    # TODO: A 100 转给 B 0 共 40，断言 A=60, B=40
    accountA = BankAccount("A", 100)
    accountB = BankAccount("B", 0)
    accountA.transfer_to(accountB, 40)
    assert accountA.balance == 60
    assert accountB.balance == 40


def test_transfer_insufficient_raises():
    # TODO: A 100 转 150 抛 ValueError，且 A、B 余额都不变
    accountA = BankAccount("A", 100)
    accountB = BankAccount("B", 0)
    with pytest.raises(ValueError) as exc_info:
        accountA.transfer_to(accountB, 150)
    assert "转账余额不足" in str(exc_info.value)


def test_transfer_negative_raises():
    # TODO: 转账 -5 抛 ValueError
    accountA = BankAccount("A", 100)
    accountB = BankAccount("B", 0)
    with pytest.raises(ValueError) as exc_info:
        accountA.transfer_to(accountB, -5)
    assert "转账金额必须大于0" in str(exc_info.value)
