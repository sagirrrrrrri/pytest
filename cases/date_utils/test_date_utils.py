"""经典案例 6 的测试：date_utils（参数化综合 + xfail）"""
import pytest

from date_utils import is_leap_year, days_in_month, parse_date, week_of_year, format_date


# ---------- 参数化：闰年 ----------
@pytest.mark.parametrize("year", [2000, 2020, 2024, 1600, 1996],
                         ids=["世纪闰年400整除", "2020闰", "2024闰", "1600闰", "1996闰"])
def test_is_leap_year_true(year):
    assert is_leap_year(year) is True


@pytest.mark.parametrize("year", [1900, 2100, 2023, 2025, 100],
                         ids=["世纪非闰100整除", "2100非闰", "2023非闰", "2025非闰", "100非闰"])
def test_is_leap_year_false(year):
    assert is_leap_year(year) is False


def test_is_leap_year_type_error():
    with pytest.raises(TypeError):
        is_leap_year("2024")


# ---------- 参数化：每月天数 ----------
@pytest.mark.parametrize("year, month, expected", [
    (2024, 1, 31),   # 大月
    (2024, 2, 29),   # 闰年二月
    (2023, 2, 28),   # 平年二月
    (2024, 4, 30),   # 小月
    (2024, 12, 31),  # 十二月
], ids=["一月31天", "闰年二月29天", "平年二月28天", "四月30天", "十二月31天"])
def test_days_in_month(year, month, expected):
    assert days_in_month(year, month) == expected


def test_days_in_month_invalid_month():
    with pytest.raises(ValueError, match="1~12"):
        days_in_month(2024, 13)


# ---------- 参数化：日期解析 ----------
@pytest.mark.parametrize("text, expected", [
    ("2024-02-29", (2024, 2, 29)),
    ("1999-12-31", (1999, 12, 31)),
    ("2026-10-10", (2026, 10, 10)),
], ids=["闰年日期", "世纪末日", "今天示例"])
def test_parse_date(text, expected):
    dt = parse_date(text)
    assert (dt.year, dt.month, dt.day) == expected


@pytest.mark.parametrize("text", ["2024-13-01", "2024-02-30", "abc", "2024/01/01", ""],
                         ids=["月份越界", "二月30日", "非日期", "斜杠格式", "空串"])
def test_parse_date_invalid(text):
    with pytest.raises(ValueError):
        parse_date(text)


# ---------- 周数 ----------
def test_week_of_year():
    # 2026-01-01 是周四，属于 ISO 2026 年第 1 周
    assert week_of_year("2026-01-01") == 1


# ---------- 格式化（strftime 自动补零） ----------
def test_format_date_with_padding():
    assert format_date(parse_date("2026-01-01")) == "2026年01月01日"


# ---------- xfail：已知待完善行为 ----------
@pytest.mark.xfail(reason="已知限制：is_leap_year 对字符串输入抛 TypeError，未来计划自动转换类型", strict=False)
def test_leap_year_string_input():
    assert is_leap_year("2024") is True   # 当前实现抛 TypeError，用例失败 → xfailed


@pytest.mark.xfail(reason="已知缺陷：负数年份未做合法性校验（-4 被误判为闰年）", strict=False)
def test_negative_year_behavior():
    assert is_leap_year(-4) is False  # 当前实现返回 True，用例失败 → xfailed
