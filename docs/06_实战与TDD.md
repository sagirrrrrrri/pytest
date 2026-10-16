# 第 6 章 实战与 TDD（测试驱动开发）

> 本章用时：约 2.5 小时。核心收获：用 TDD 流程从零开发一个小项目，并学会给已有代码补测试。

---

## 6.1 什么是 TDD

TDD（Test-Driven Development，测试驱动开发）循环：

```
写一个会失败的测试（红）
        ↓
写最少代码让它通过（绿）
        ↓
重构代码（保持测试通过）（重构）
        ↓
    下一个需求
```

核心思想：**先定义"什么算对"，再实现"让它对"**。

TDD 的收益：

- 代码永远有测试覆盖（不是事后补）；
- 逼迫你先想清楚行为边界（输入、输出、异常）；
- 天然形成"可测试的设计"（耦合度低）。

---

## 6.2 实战演练：购物车（完整 TDD 过程）

我们来实现一个购物车类。完整代码见 `cases/shopping_cart/`，这里展示 TDD 过程的关键步骤。

**第 1 步：写第一个失败测试**（红）

```python
# test_shopping_cart.py（先写测试！）
from shopping_cart import ShoppingCart


def test_add_item():
    cart = ShoppingCart()
    cart.add_item("苹果", price=5.0, quantity=2)
    assert cart.items == {"苹果": {"price": 5.0, "quantity": 2}}
```

运行 → 失败（`ModuleNotFoundError: shopping_cart`）。**失败正是我们要的**：它定义了第一个需求。

**第 2 步：写最少代码让它通过**（绿）

```python
# shopping_cart.py
class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, name, price, quantity=1):
        self.items[name] = {"price": price, "quantity": quantity}
```

运行 → 通过。

**第 3 步：写下一个失败测试，重复循环**

```python
def test_total_price():
    cart = ShoppingCart()
    cart.add_item("苹果", 5.0, 2)
    cart.add_item("香蕉", 3.0, 3)
    assert cart.total_price() == pytest.approx(19.0)
```

失败 → 实现：

```python
def total_price(self):
    return sum(item["price"] * item["quantity"] for item in self.items.values())
```

通过 → 继续。

**第 4 步：异常路径**

```python
def test_add_negative_price_raises():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="价格不能为负"):
        cart.add_item("苹果", -5.0)
```

实现：

```python
def add_item(self, name, price, quantity=1):
    if price < 0:
        raise ValueError("价格不能为负")
    ...
```

如此循环，直到所有需求都有测试且通过。**需求清单就是你的测试清单**。

---

## 6.3 给已有代码补测试（重要技能）

很多场景是"代码已经写好了，现在要补测试"。步骤：

1. **通读代码**，列出每个函数/方法的：
   - 输入（正常、边界、非法）；
   - 输出；
   - 异常；
   - 副作用（写文件、发请求、改全局状态）。
2. 每个"输入→输出"写一条测试；非法输入写 `raises` 测试。
3. 有外部依赖（网络/文件/时间）用 mock 隔离。
4. 先跑出覆盖率，再补缺口。

**补测试示例**：

```python
# 已有业务代码
def discount_price(price, discount):
    """打折扣：discount 0~0.9，非法抛 ValueError"""
    if not 0 <= discount <= 0.9:
        raise ValueError("折扣需在 0~0.9 之间")
    return round(price * (1 - discount), 2)
```

```python
# 补的测试
import pytest
from pricing import discount_price


@pytest.mark.parametrize("price, discount, expected", [
    (100, 0, 100.0),
    (100, 0.1, 90.0),
    (100, 0.9, 10.0),
    (59.9, 0.2, 47.92),
], ids=["不打折", "九折", "一折", "带小数"])
def test_discount_price(price, discount, expected):
    assert discount_price(price, discount) == pytest.approx(expected)


@pytest.mark.parametrize("price, discount", [
    (100, -0.1),
    (100, 1.0),
    (100, 0.95),
], ids=["负折扣", "折扣超上限", "折扣不在区间"])
def test_discount_invalid(price, discount):
    with pytest.raises(ValueError, match="折扣"):
        discount_price(price, discount)
```

---

## 6.4 测试可维护性指南

1. **一个测试只验证一个行为**，失败时一眼定位；
2. **测试名要像句子**：`test_add_item_increases_total` 比 `test_1` 好；
3. **避免测试间共享可变状态**：共享 fixture 用 yield 清理；
4. **别测实现细节**：测"行为/结果"，不测"内部调用了哪个私有方法"；
5. **测试也遵循 DRY**：重复准备逻辑提取成 fixture；
6. **固定随机性**：mock 掉 `random` / `time.time()`，保证可重复。

---

## 6.5 如何组织一次"开发+测试"的工作流（实操建议）

```
① 想清楚需求，写成清单（要做什么、边界在哪）
② 为每个需求写一条失败测试
③ 每通过一条，就提交一次（git commit：红→绿记录清晰）
④ 全部通过后，运行覆盖率看缺口
⑤ 重构：保持测试全绿的前提下优化代码
⑥ 定期跑：py312 -m pytest
```

推荐练习节奏：**每个经典案例都先用 TDD 重写一遍**，再对照参考答案。

---

## 6.6 常见坑

1. **跳过"写失败测试"直接实现**：这是最常见的 TDD 走样。失败测试证明"测试真的能抓错"。
2. **一个测试塞多个断言**：定位失败变难。
3. **测试依赖真实外部资源**（真发邮件、真连数据库）：慢、脆弱、不可重复——一律 mock。
4. **只测 happy path**：异常、边界（空、极大、极小、重复）才是 bug 高发区。
5. **为了覆盖率凑断言**：`assert True` 不算测试。

---

## 6.7 自测题

1. TDD 的三步循环是什么？
2. 为什么说"写失败测试"是 TDD 的必要步骤？
3. 给已有代码补测试时，如何枚举测试点？
4. 测试中如何固定随机行为？
5. 测试名 `test_1` 和 `test_discount_rejects_over_limit` 哪个好？为什么？

---

## 本章小结

- TDD：红 → 绿 → 重构，需求清单即测试清单；
- 补测试：枚举输入/输出/异常/副作用，mock 外部依赖；
- 可维护性：单行为、好名字、无共享可变状态、测行为不测实现；
- 到这里，pytest 的核心已全部覆盖。接下来：经典案例逐行阅读 → 独立完成练习 → 综合实战。
