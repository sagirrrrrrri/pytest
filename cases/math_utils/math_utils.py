"""
经典案例 1：数学工具函数
覆盖知识点：基础断言、pytest.raises、参数化、approx
运行方式：py312 -m pytest test_math_utils.py -v
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    """除法：除数为 0 抛 ZeroDivisionError"""
    if b == 0:
        raise ZeroDivisionError("除数不能为 0")
    return a / b


def factorial(n):
    """阶乘：n 必须是非负整数"""
    if not isinstance(n, int) or n < 0:
        raise ValueError("阶乘要求非负整数")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def is_prime(n):
    """判断素数"""
    if not isinstance(n, int) or n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def average(numbers):
    """求平均值：空列表抛 ValueError"""
    if not numbers:
        raise ValueError("列表不能为空")
    return sum(numbers) / len(numbers)
