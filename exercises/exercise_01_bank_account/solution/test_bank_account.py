"""练习 1 参考答案：完整测试"""
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
    account = BankAccount("小明", 100.0)
    new_balance = account.deposit(50)
    assert new_balance == pytest.approx(150.0)
    assert account.balance == pytest.approx(150.0)


def test_deposit_zero_raises():
    account = BankAccount("小明")
    with pytest.raises(ValueError, match="大于 0"):
        account.deposit(0)


def test_deposit_negative_raises():
    account = BankAccount("小明")
    with pytest.raises(ValueError, match="大于 0"):
        account.deposit(-10)


# ---------- 取款 ----------
def test_withdraw():
    account = BankAccount("小明", 100.0)
    new_balance = account.withdraw(30)
    assert new_balance == pytest.approx(70.0)


def test_withdraw_over_balance_raises():
    account = BankAccount("小明", 100.0)
    with pytest.raises(ValueError, match="余额不足"):
        account.withdraw(150)
    assert account.balance == pytest.approx(100.0)  # 状态未变


def test_withdraw_zero_raises():
    account = BankAccount("小明", 100.0)
    with pytest.raises(ValueError, match="大于 0"):
        account.withdraw(0)


# ---------- 转账 ----------
def test_transfer():
    alice = BankAccount("小明", 100.0)
    bob = BankAccount("小玉", 0.0)
    alice.transfer_to(bob, 40)
    assert alice.balance == pytest.approx(60.0)
    assert bob.balance == pytest.approx(40.0)


def test_transfer_insufficient_raises():
    alice = BankAccount("小明", 100.0)
    bob = BankAccount("小玉", 0.0)
    with pytest.raises(ValueError, match="余额不足"):
        alice.transfer_to(bob, 150)
    assert alice.balance == pytest.approx(100.0)  # 双方余额都不变
    assert bob.balance == pytest.approx(0.0)


def test_transfer_negative_raises():
    alice = BankAccount("小明", 100.0)
    bob = BankAccount("小玉", 0.0)
    with pytest.raises(ValueError, match="大于 0"):
        alice.transfer_to(bob, -5)
