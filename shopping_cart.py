class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, name, price, quantity=1):
        if price < 0:
            raise ValueError("价格不能为负")
        self.items[name] = {"price": price, "quantity": quantity}

    def total_price(self):
        total = 0
        for item in self.items.values():
            total += item["price"] * item["quantity"]
        return total


def discount_price(price, discount):
    if not 0 <= discount <= 0.9:
        raise ValueError("折扣需在0-0.9之间")
    return round(price * (1 - discount), 2)
