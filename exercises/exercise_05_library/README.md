# 练习 5：图书馆借阅系统（综合 TDD 实战）

> 难度：★★★★☆ | 对应文档：第 6 章（+ 全章节综合）| 预计 1~1.5 小时

这是整套练习的**毕业项目**：用 TDD 流程从零实现一个小型图书管理系统，并配上完整测试。

## 任务

用 **TDD（红 → 绿 → 重构）** 实现 `Library` 类。

## 需求

```python
class Book:
    """图书：isbn, title, author, available(bool)"""


class Library:
    def __init__(self):
        """内部维护 books 字典（key=isbn）"""

    def add_book(self, isbn, title, author) -> None:
        """添加图书；isbn 已存在抛 ValueError("ISBN 已存在")"""

    def borrow(self, isbn, user) -> None:
        """借书：记录借阅人；不存在抛 KeyError；已被借出抛 ValueError("已被借出")"""

    def return_book(self, isbn) -> None:
        """还书：恢复可借状态；未被借出抛 ValueError("未被借出")"""

    def search_by_title(self, keyword) -> list:
        """按书名模糊搜索（不区分大小写），返回匹配的 Book 列表"""

    def available_books(self) -> list:
        """返回所有可借的图书列表"""

    def borrowed_by(self, user) -> list:
        """返回某用户当前借走的图书列表"""

    @property
    def total_count(self) -> int:
        """馆藏总数"""
```

## TDD 流程（务必按顺序做）

1. **第 1 个失败测试**：`test_add_book`（添加后 `total_count == 1`）→ 运行看到失败；
2. **最少实现**：`Book` + `Library.__init__` + `add_book` → 绿；
3. **下一个测试**：`test_borrow_and_return` → 红 → 实现 `borrow`/`return_book` → 绿；
4. 依次推进：重复 ISBN → 借出状态流转 → 搜索 → 用户借阅列表；
5. 全部绿后，检查覆盖率（`--cov`），补缺口；
6. 重构：让代码更整洁，保持全绿。

## 验收标准

- 至少 **12 个测试**，全部通过；
- 覆盖：正常流程、异常（重复 ISBN / 借不存在 / 借已借出 / 还未借出就还）、搜索边界；
- 每个方法都有测试（可用 `--cov=library --cov-report=term-missing` 检查）；
- 测试名能读成句子：`test_borrow_twice_raises`。

## 运行方式

```powershell
cd "G:\QA2\pytest\exercises\exercise_05_library"
py312 -m pytest test_library.py -v
# 覆盖率检查：
py312 -m pytest --cov=library --cov-report=term-missing
```

写完后对照 `solution/` 参考答案（参考答案只是其中一种写法，你的实现可以更好）。
