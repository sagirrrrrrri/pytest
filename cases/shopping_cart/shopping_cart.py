"""
经典案例 4：购物车（类 + fixture + 状态测试）
覆盖知识点：类测试、fixture 注入、yield 清理、参数化、异常、边界
运行方式：py312 -m pytest test_shopping_cart.py -v
"""


class ShoppingCart:
    """购物车：管理商品、价格、数量与结算"""

    def __init__(self):
        # items: {商品名: {"price": float, "quantity": int}}
        self.items = {}

    def add_item(self, name: str, price: float, quantity: int = 1) -> None:
        if price < 0:
            raise ValueError("价格不能为负")
        if quantity <= 0:
            raise ValueError("数量必须大于 0")
        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"price": float(price), "quantity": quantity}

    def remove_item(self, name: str, quantity: int = 1) -> None:
        if name not in self.items:
            raise KeyError(f"购物车中没有该商品: {name}")
        self.items[name]["quantity"] -= quantity
        if self.items[name]["quantity"] <= 0:
            del self.items[name]

    def total_price(self) -> float:
        """所有商品总价（不打折）"""
        return round(
            sum(i["price"] * i["quantity"] for i in self.items.values()), 2
        )

    def apply_discount(self, rate: float) -> float:
        """按折扣率结算：rate 0~0.9"""
        if not 0 <= rate <= 0.9:
            raise ValueError("折扣率需在 0~0.9 之间")
        return round(self.total_price() * (1 - rate), 2)

    def clear(self) -> None:
        self.items.clear()

    @property
    def item_count(self) -> int:
        """商品种类数"""
        return len(self.items)
