"""
经典案例 6：日期工具（参数化 + xfail + 边界）
覆盖知识点：参数化综合、xfail 预期失败、边界输入、datetime
运行方式：py312 -m pytest test_date_utils.py -v
"""
from datetime import datetime


def is_leap_year(year: int) -> bool:
    """闰年判断：能被 400 整除，或能被 4 整除但不能被 100 整除"""
    if not isinstance(year, int):
        raise TypeError("年份必须是整数")
    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)


def days_in_month(year: int, month: int) -> int:
    """返回某年某月的天数"""
    if month < 1 or month > 12:
        raise ValueError("月份必须在 1~12 之间")
    days_31 = {1, 3, 5, 7, 8, 10, 12}
    if month in days_31:
        return 31
    if month == 2:
        return 29 if is_leap_year(year) else 28
    return 30


def parse_date(text: str) -> datetime:
    """解析 YYYY-MM-DD 格式的日期字符串"""
    try:
        return datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"日期格式应为 YYYY-MM-DD: {text}")


def week_of_year(text: str) -> int:
    """返回 ISO 周数"""
    return parse_date(text).isocalendar().week


def format_date(dt: datetime) -> str:
    """格式化为 YYYY年MM月DD日"""
    return dt.strftime("%Y年%m月%d日")
