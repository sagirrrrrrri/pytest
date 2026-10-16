"""练习 5 参考答案：library 完整测试"""
import pytest

from library import Library


@pytest.fixture
def lib():
    return Library()


@pytest.fixture
def lib_with_books(lib):
    lib.add_book("978-1", "Python 入门", "小明")
    lib.add_book("978-2", "Pytest 实战", "小玉")
    lib.add_book("978-3", "数据分析基础", "小红")
    return lib


# ---------- 添加图书 ----------
def test_add_book(lib):
    lib.add_book("978-1", "Python 入门", "小明")
    assert lib.total_count == 1


def test_add_duplicate_isbn_raises(lib):
    lib.add_book("978-1", "Python 入门", "小明")
    with pytest.raises(ValueError, match="已存在"):
        lib.add_book("978-1", "另一本", "小红")


# ---------- 借书 ----------
def test_borrow_success(lib_with_books):
    lib_with_books.borrow("978-1", "小明")
    titles = [b.title for b in lib_with_books.available_books()]
    assert "Python 入门" not in titles
    assert len(lib_with_books.available_books()) == 2


def test_borrow_missing_isbn_raises(lib):
    with pytest.raises(KeyError, match="不存在"):
        lib.borrow("000-0", "小明")


def test_borrow_twice_raises(lib_with_books):
    lib_with_books.borrow("978-1", "小明")
    with pytest.raises(ValueError, match="已被借出"):
        lib_with_books.borrow("978-1", "小玉")


# ---------- 还书 ----------
def test_return_book(lib_with_books):
    lib_with_books.borrow("978-1", "小明")
    lib_with_books.return_book("978-1")
    titles = [b.title for b in lib_with_books.available_books()]
    assert "Python 入门" in titles
    assert len(lib_with_books.available_books()) == 3


def test_return_not_borrowed_raises(lib_with_books):
    with pytest.raises(ValueError, match="未被借出"):
        lib_with_books.return_book("978-1")


# ---------- 搜索 ----------
def test_search_by_title_keyword(lib_with_books):
    assert len(lib_with_books.search_by_title("python")) == 1
    assert len(lib_with_books.search_by_title("基础")) == 1


def test_search_by_title_case_insensitive(lib_with_books):
    assert len(lib_with_books.search_by_title("PYTHON")) == 1
    assert len(lib_with_books.search_by_title("PyThOn")) == 1


def test_search_no_match(lib_with_books):
    assert lib_with_books.search_by_title("不存在") == []


# ---------- 用户借阅 ----------
def test_borrowed_by(lib_with_books):
    lib_with_books.borrow("978-1", "小明")
    lib_with_books.borrow("978-3", "小红")
    ming_titles = [b.title for b in lib_with_books.borrowed_by("小明")]
    hong_titles = [b.title for b in lib_with_books.borrowed_by("小红")]
    assert ming_titles == ["Python 入门"]
    assert hong_titles == ["数据分析基础"]
    assert lib_with_books.borrowed_by("小玉") == []


def test_borrowed_by_none(lib):
    assert lib.borrowed_by("小明") == []


# ---------- 综合状态 ----------
def test_full_borrow_return_cycle(lib_with_books):
    lib_with_books.borrow("978-2", "小明")
    assert len(lib_with_books.borrowed_by("小明")) == 1

    lib_with_books.return_book("978-2")
    assert lib_with_books.borrowed_by("小明") == []
    assert "Pytest 实战" in [b.title for b in lib_with_books.available_books()]

    lib_with_books.borrow("978-2", "小玉")   # 可以再次借出
    assert len(lib_with_books.borrowed_by("小玉")) == 1
