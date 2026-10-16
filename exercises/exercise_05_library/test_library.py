"""练习 5 的测试骨架：先实现 library.py，再按 TDD 顺序补全测试"""

import pytest

from library import Library


@pytest.fixture
def lib():
    """每个测试独立的图书馆"""
    return Library()


@pytest.fixture
def lib_with_books(lib):
    """预置 3 本图书的图书馆（fixture 依赖 fixture）"""
    lib.add_book("978-1", "Python 入门", "小明")
    lib.add_book("978-2", "Pytest 实战", "小玉")
    lib.add_book("978-3", "数据分析基础", "小红")
    return lib


# ---------- 添加图书 ----------
def test_add_book(lib):
    # TODO: add_book 后 total_count == 1
    lib.add_book("978-4", "自动化测试", "小刚")
    assert lib.total_count == 1


def test_add_duplicate_isbn_raises(lib):
    # TODO: 添加两次同一 ISBN 抛 ValueError
    lib.add_book("978-4", "自动化测试", "小刚")
    with pytest.raises(ValueError):
        lib.add_book("978-4", "自动化测试1", "小刚1")


# ---------- 借书 ----------
def test_rowbor_success(lib_with_books):
    # TODO: 借 978-1 成功，available_books 不再包含它
    lib_with_books.borrow("978-1", "小明")
    assert "978-1" not in [b.isbn for b in lib_with_books.available_books()]


def test_borrow_missing_isbn_raises(lib):
    # TODO: 借不存在的 ISBN 抛 KeyError
    with pytest.raises(KeyError):
        lib.borrow("978-1", "小明")


def test_borrow_twice_raises(lib_with_books):
    # TODO: 同一本书借两次，第二次抛 ValueError
    lib_with_books.borrow("978-1", "小明")
    with pytest.raises(ValueError):
        lib_with_books.borrow("978-1", "小明")


# ---------- 还书 ----------
def test_return_book(lib_with_books):
    # TODO: 借出再归还，available_books 恢复包含它
    lib_with_books.borrow("978-1", "小明")
    lib_with_books.return_book("978-1")
    assert "978-1" in [b.isbn for b in lib_with_books.available_books()]


def test_return_not_borrowed_raises(lib_with_books):
    # TODO: 没借过就还，抛 ValueError
    with pytest.raises(ValueError):
        lib_with_books.return_book("978-1")


# ---------- 搜索 ----------
def test_search_by_title_keyword(lib_with_books):
    # TODO: 搜 "python" 命中 1 本；搜 "基础" 命中 1 本
    assert len(lib_with_books.search_by_title("基础")) == 1


def test_search_by_title_case_insensitive(lib_with_books):
    # TODO: 搜 "PYTHON" 也能命中
    assert lib_with_books.search_by_title("PYTHON") != []


def test_search_no_match(lib_with_books):
    # TODO: 搜 "不存在" 返回空列表
    assert lib_with_books.search_by_title("不存在") == []


# ---------- 用户借阅 ----------
def test_borrowed_by(lib_with_books):
    # TODO: 小明借 1 本，小红借 1 本；borrowed_by("小明") 返回对应图书
    lib_with_books.borrow("978-1", "小明")
    lib_with_books.borrow("978-2", "小玉")
    assert [b.isbn for b in lib_with_books.borrowed_by("小明")] == ["978-1"]


def test_borrowed_by_none(lib):
    # TODO: 没人借过书时返回空列表
    assert lib.borrowed_by("小明") == []


# ---------- 综合状态 ----------
def test_full_borrow_return_cycle(lib_with_books):
    # TODO: 借出→归还→再借出，验证状态流转正确
    lib_with_books.borrow("978-2", "小玉")
    assert "978-2" not in [b.isbn for b in lib_with_books.available_books()]
    lib_with_books.return_book("978-2")
    assert "978-2" in [b.isbn for b in lib_with_books.available_books()]
    lib_with_books.borrow("978-2", "小红")
    assert "978-2" not in [b.isbn for b in lib_with_books.available_books()]


###py312 -m pytest test_library.py -v
