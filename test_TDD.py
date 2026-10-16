#     python -m pytest test_TDD.py

import pytest
from shopping_cart import ShoppingCart, discount_price


def test_add_item():
    cart = ShoppingCart()
    cart.add_item("苹果", price=5.0, quantity=2)
    assert cart.items == {"苹果": {"price": 5.0, "quantity": 2}}


def test_total_price():
    cart = ShoppingCart()
    cart.add_item("苹果", 5.0, 2)
    cart.add_item("香蕉", 3.0, 3)
    assert cart.total_price() == pytest.approx(19.0)


def test_add_negative_price_raises():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="价格不能为负"):
        cart.add_item("苹果", -5.0)


@pytest.mark.parametrize(
    "price, discount, expected",
    [
        (100, 0, 100.0),
        (100, 0.1, 90.0),
        (100, 0.9, 10.0),
        (59.9, 0.2, 47.92),
    ],
    ids=["不打折", "九折", "一折", "带小数"],
)
def test_discount_price(price, discount, expected):
    assert discount_price(price, discount) == pytest.approx(expected)


@pytest.mark.parametrize(
    "price, discount",
    [
        (100, -0.1),
        (100, 1.0),
        (100, 0.95),
    ],
    ids=["负折扣", "折扣超上限", "折扣不在区间"],
)
def test_discount_invalid(price, discount):
    with pytest.raises(ValueError, match="折扣"):
        discount_price(price, discount)
