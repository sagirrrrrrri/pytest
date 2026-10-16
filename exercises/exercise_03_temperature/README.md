# 练习 3：温度转换（参数化）

> 难度：★★☆☆☆ | 对应文档：第 4 章 | 预计 30 分钟

## 任务

实现温度转换工具 `TemperatureConverter`，重点练习 `parametrize` 参数化测试。

## 需求

```python
class TemperatureConverter:
    @staticmethod
    def c_to_f(celsius: float) -> float:
        """摄氏 → 华氏：F = C * 9/5 + 32"""

    @staticmethod
    def f_to_c(fahrenheit: float) -> float:
        """华氏 → 摄氏：C = (F - 32) * 5/9"""

    @staticmethod
    def c_to_k(celsius: float) -> float:
        """摄氏 → 开尔文：K = C + 273.15；结果低于 0K 抛 ValueError（绝对零度以下）"""

    @staticmethod
    def k_to_c(kelvin: float) -> float:
        """开尔文 → 摄氏：C = K - 273.15；K < 0 抛 ValueError"""
```

## 要求

1. **所有转换测试都用 `parametrize` 写**，每组数据一个用例；
2. 至少包含：整数、负数、浮点、特殊值（如 0°C、100°C、-40°C——华氏摄氏相等点）；
3. 非法输入（低于绝对零度）用 `parametrize` + `raises` 组合测试；
4. 使用 `pytest.approx` 比较浮点结果；
5. 用 `ids` 给用例起名。

## 运行方式

```powershell
cd "G:\QA2\pytest\exercises\exercise_03_temperature"
py312 -m pytest test_temperature.py -v
```

## 提示

- `-40°C == -40°F` 是经典测试数据（`c_to_f(-40) == -40`）；
- 开尔文不允许负数：`c_to_k(-300)` 会低于 0K，应抛 `ValueError`；
- `ids` 写法：`ids=["0°C", "100°C", ...]`，注意与参数组数一一对应；
- 用 `match` 校验异常信息。

写完后对照 `solution/` 参考答案。
