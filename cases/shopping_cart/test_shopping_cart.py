"""经典案例 4 的测试：shopping_cart（类测试 + fixture 工厂）"""
import pytest

from shopping_cart import ShoppingCart


@pytest.fixture
def cart():
    """每个测试一个全新购物车（function 级，天然隔离）"""
    return ShoppingCart()


@pytest.fixture
def filled_cart(cart):
    """工厂思路：在 cart 基础上预置商品（fixture 依赖 fixture）"""
    cart.add_item("苹果", 5.0, 2)
    cart.add_item("香蕉", 3.0, 3)
    return cart


# ---------- 添加商品 ----------
def test_add_item(cart):
    cart.add_item("苹果", 5.0, 2)
    assert cart.items["苹果"] == {"price": 5.0, "quantity": 2}


def test_add_same_item_increases_quantity(cart):
    cart.add_item("苹果", 5.0, 2)
    cart.add_item("苹果", 5.0, 3)
    assert cart.items["苹果"]["quantity"] == 5


def test_add_item_default_quantity(cart):
    cart.add_item("苹果", 5.0)
    assert cart.items["苹果"]["quantity"] == 1


# ---------- 非法参数 ----------
@pytest.mark.parametrize("price, quantity", [
    (-1, 1),
    (5, 0),
    (5, -2),
], ids=["负价格", "零数量", "负数量"])
def test_add_item_invalid(cart, price, quantity):
    with pytest.raises(ValueError):
        cart.add_item("苹果", price, quantity)


# ---------- 删除商品 ----------
def test_remove_item(cart):
    cart.add_item("苹果", 5.0, 2)
    cart.remove_item("苹果", 1)
    assert cart.items["苹果"]["quantity"] == 1


def test_remove_to_zero_deletes_key(cart):
    cart.add_item("苹果", 5.0, 2)
    cart.remove_item("苹果", 2)
    assert "苹果" not in cart.items


def test_remove_missing_raises(cart):
    with pytest.raises(KeyError, match="没有该商品"):
        cart.remove_item("橙子")


# ---------- 总价与折扣（fixture 依赖演示） ----------
def test_total_price(filled_cart):
    assert filled_cart.total_price() == pytest.approx(5.0 * 2 + 3.0 * 3)


def test_total_price_empty_cart(cart):
    assert cart.total_price() == 0


@pytest.mark.parametrize("rate, expected_total", [
    (0, 19.0),
    (0.1, 17.1),
    (0.5, 9.5),
    (0.9, 1.9),
], ids=["不打折", "九折", "五折", "一折"])
def test_apply_discount(filled_cart, rate, expected_total):
    assert filled_cart.apply_discount(rate) == pytest.approx(expected_total)


def test_discount_invalid_rate(filled_cart):
    with pytest.raises(ValueError, match="0~0.9"):
        filled_cart.apply_discount(1.0)


# ---------- 其他 ----------
def test_item_count(cart):
    cart.add_item("a", 1.0)
    cart.add_item("b", 2.0)
    assert cart.item_count == 2


def test_clear(cart):
    cart.add_item("a", 1.0)
    cart.clear()
    assert cart.item_count == 0
    assert cart.total_price() == 0
