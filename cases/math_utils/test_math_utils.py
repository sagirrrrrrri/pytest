"""经典案例 1 的测试：math_utils"""
import pytest

from math_utils import add, subtract, multiply, divide, factorial, is_prime, average


# ---------- 1. 基础断言 ----------
def test_add():
    assert add(1, 2) == 3


def test_subtract_negative_result():
    assert subtract(2, 10) == -8


# ---------- 2. 异常断言 ----------
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="除数"):
        divide(10, 0)


def test_factorial_negative():
    with pytest.raises(ValueError):
        factorial(-3)


def test_average_empty_list():
    with pytest.raises(ValueError, match="不能为空"):
        average([])


# ---------- 3. 参数化（数据驱动） ----------
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (-1, 1, 0),
    (0, 0, 0),
    (10, -5, 5),
    (2.5, 2.5, 5.0),
], ids=["正整数", "互为相反数", "双零", "一正一负", "浮点数"])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (1, 1),
    (5, 120),
    (10, 3628800),
], ids=["0!", "1!", "5!", "10!"])
def test_factorial_parametrized(n, expected):
    assert factorial(n) == expected


@pytest.mark.parametrize("n, expected", [
    (2, True),
    (3, True),
    (4, False),
    (17, True),
    (1, False),
    (0, False),
    (-7, False),
], ids=["2质数", "3质数", "4合数", "17质数", "1非质数", "0非质数", "负数"])
def test_is_prime_parametrized(n, expected):
    assert is_prime(n) is expected


# ---------- 4. 浮点数比较 ----------
def test_average_with_float():
    assert average([0.1, 0.2, 0.3]) == pytest.approx(0.2)


# ---------- 5. 多个断言配合（相关联时允许） ----------
def test_multiply_commutative():
    assert multiply(3, 4) == 12
    assert multiply(4, 3) == 12
