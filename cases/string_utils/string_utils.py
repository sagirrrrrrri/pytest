"""
经典案例 2：字符串处理工具
覆盖知识点：参数化（经典用法）、边界输入、异常、ids
运行方式：py312 -m pytest test_string_utils.py -v
"""


def reverse(s):
    """反转字符串"""
    return s[::-1]


def is_palindrome(s):
    """判断回文（忽略大小写、空白与标点，只保留字母数字）"""
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]


def count_vowels(s):
    """统计英文元音字母个数（a/e/i/o/u，不区分大小写）"""
    return sum(1 for ch in s.lower() if ch in "aeiou")


def to_snake_case(text):
    """
    驼峰/空格/连字符 → 下划线小写。
    规则：大写字母前若满足以下任一条件则加分隔下划线：
    1) 前一个字符是小写字母或数字；
    2) 前面是连续大写、但当前字母后紧跟小写字母（如 HTTPRequest → http_request）。
    """
    if not text:
        return ""
    result = []
    for i, ch in enumerate(text):
        if ch.isupper():
            if i > 0:
                prev = text[i - 1]
                if prev.islower() or prev.isdigit():
                    result.append("_")
                elif prev.isupper() and i + 1 < len(text) and text[i + 1].islower():
                    result.append("_")
            result.append(ch.lower())
        elif ch in " -":
            result.append("_")
        else:
            result.append(ch)
    return "".join(result).replace("__", "_").strip("_")


def truncate(s, max_len):
    """截断字符串：超过 max_len 加省略号"""
    if max_len < 1:
        raise ValueError("max_len 必须大于 0")
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."
