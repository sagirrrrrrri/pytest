"""经典案例 2 的测试：string_utils"""
import pytest

from string_utils import reverse, is_palindrome, count_vowels, to_snake_case, truncate


# ---------- 参数化：反转 ----------
@pytest.mark.parametrize("s, expected", [
    ("abc", "cba"),
    ("", ""),
    ("a", "a"),
    ("你好世界", "界世好你"),
    ("racecar", "racecar"),
], ids=["普通字符串", "空串", "单字符", "中文", "回文本身"])
def test_reverse(s, expected):
    assert reverse(s) == expected


# ---------- 参数化：回文 ----------
@pytest.mark.parametrize("s, expected", [
    ("racecar", True),
    ("A man a plan a canal Panama", True),
    ("No 'x' in Nixon", True),
    ("hello", False),
    ("", True),          # 空串视为回文
], ids=["单词回文", "含空格回文", "标点回文", "非回文", "空串"])
def test_is_palindrome(s, expected):
    assert is_palindrome(s) is expected


# ---------- 参数化：元音统计 ----------
@pytest.mark.parametrize("s, expected", [
    ("hello", 2),
    ("AEIOU", 5),
    ("bcdfg", 0),
    ("", 0),
    ("Python is fun", 3),
], ids=["hello两元音", "全大写元音", "无元音", "空串", "含空格"])
def test_count_vowels(s, expected):
    assert count_vowels(s) == expected


# ---------- 参数化：蛇形命名 ----------
@pytest.mark.parametrize("text, expected", [
    ("HelloWorld", "hello_world"),
    ("helloWorld", "hello_world"),
    ("HTTPRequest", "http_request"),
    ("hello world", "hello_world"),
    ("get-user-info", "get_user_info"),
    ("", ""),
], ids=["大驼峰", "小驼峰", "连续大写", "空格分隔", "连字符", "空串"])
def test_to_snake_case(text, expected):
    assert to_snake_case(text) == expected


# ---------- 异常与边界 ----------
def test_truncate_short_string_unchanged():
    assert truncate("abc", 10) == "abc"


def test_truncate_long_string():
    result = truncate("hello world python", 10)
    assert len(result) == 10
    assert result.endswith("...")


def test_truncate_chinese():
    result = truncate("这是一个很长的字符串内容", 8)
    # s[:5] = "这是一个很"（5 个字符）+ "..." = 8 个字符
    assert result == "这是一个很..."
    assert len(result) == 8


def test_truncate_invalid_max_len():
    with pytest.raises(ValueError, match="必须大于"):
        truncate("abc", 0)
