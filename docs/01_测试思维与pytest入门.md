# 第 1 章 测试思维与 pytest 入门

> 目标读者：已学完 Python 基础（变量、函数、类、异常、文件读写）。
> 本章用时：约 1.5 小时。核心收获：理解"为什么要测试"，能写出并运行第一个 pytest 测试。

---

## 1.1 为什么要写测试

写代码的人通常有这种经历：改了一个函数，结果把另一个功能弄坏了；上线前"手动点一遍"很累，还总漏。

**自动化测试的价值**：

| 好处 | 说明 |
| --- | --- |
| 回归保护 | 改代码后跑一遍测试，立刻知道有没有改坏东西 |
| 文档作用 | 测试本身就是"代码该怎么用"的最好示例 |
| 倒逼设计 | 写测试会发现代码耦合太紧、难以测试，促使你写出更干净的代码 |
| 加速开发 | 一次配好，之后每次修改几秒钟就能验证 |

**测试金字塔**（从多到少）：
```
        /\    UI 端到端测试（少、慢、贵）
       /  \   集成测试（中）
      /____\  单元测试（多、快、便宜）← pytest 最擅长这层
```

pytest 主要写**单元测试**：直接调用一个函数、操作一个类，验证其行为。

---

## 1.2 环境确认

本套学习计划使用的 Python 位于 `G:\Python312`（3.12.10），pytest 及插件已配好。

在终端（PowerShell）验证：

```powershell
& "G:\Python312\python.exe" -m pytest --version
```

输出应包含 `pytest 9.1.1`。

> 技巧：每次都敲 `& "G:\Python312\python.exe"` 太啰嗦，可在 PowerShell 里做一次映射：
> ```powershell
> Set-Alias py312 "G:\Python312\python.exe"
> py312 -m pytest --version
> ```

---

## 1.3 第一个测试

新建文件 `test_first.py`，内容：

```python
# test_first.py
def add(a, b):
    return a + b


def test_add():
    assert add(1, 2) == 3


def test_add_negative():
    assert add(-1, 5) == 4
```

在文件所在目录运行：

```powershell
py312 -m pytest test_first.py
```

输出：

```
collected 2 items
test_first.py ..                                              [100%]
2 passed in 0.02s
```

**核心规则（务必记住）**：

1. 测试文件名以 `test_` 开头（或 `_test` 结尾），pytest 才会收集；
2. 测试函数名以 `test_` 开头；
3. 测试函数内部用 `assert` 判断结果是否符合预期；
4. 一个函数就是一个测试用例；断言失败，该用例就失败。

---

## 1.4 常用运行方式

| 命令 | 作用 |
| --- | --- |
| `py312 -m pytest` | 递归收集当前目录所有测试 |
| `py312 -m pytest test_first.py` | 只跑指定文件 |
| `py312 -m pytest -v` | verbose，显示每个用例名与结果 |
| `py312 -m pytest -k "add"` | 按名称关键字筛选（可写 `-k "add and not negative"`） |
| `py312 -m pytest -x` | 遇到第一个失败就停 |
| `py312 -m pytest --maxfail=3` | 最多允许 3 个失败 |
| `py312 -m pytest -s` | 显示测试中的 print 输出 |
| `py312 -m pytest --lf` | 只重跑上次失败的用例 |
| `py312 -m pytest --collect-only` | 只列出收集到的用例，不执行 |

写一个故意失败的测试试试：

```python
def test_fail_demo():
    assert 1 + 1 == 3
```

运行 `py312 -m pytest test_first.py -v`，你会看到类似：

```
____________________________ test_fail_demo _____________________________
    def test_fail_demo():
>       assert 1 + 1 == 3
E       assert 2 == 3
```

pytest 会把失败的断言**重新计算并展示两边实际值**，这是它比 `unittest` 体验好的关键之一。

---

## 1.5 assert 初识（第 2 章会展开）

`assert 表达式` 等价于"如果表达式为假，抛 AssertionError"。pytest 会拦截 AssertionError 并美化输出。

```python
def test_assert_demo():
    nums = [1, 2, 3]
    assert 2 in nums          # 成员判断
    assert len(nums) == 3     # 长度判断
    assert nums[0] == 1       # 值判断
    assert nums == [1, 2, 3]  # 容器整体比较
    assert {"a": 1} == {"a": 1}  # 字典比较
```

> 与 `if...raise` 的区别：测试里就用 `assert`，不要写 `if x != 3: raise ...`。

---

## 1.6 常见坑

1. **测试函数名没以 test 开头** → 用例被静默忽略。用 `--collect-only` 检查收集结果。
2. **在函数外写逻辑**：模块顶层只放函数/类定义与常量，别放执行语句，否则 import 时会被执行。
3. **依赖执行顺序**：每个测试函数应当互相独立，不依赖"上一个测试先跑"。
4. **用 `if __name__ == "__main__"` 把演示代码包起来**，避免被测试收集时执行。

---

## 1.7 自测题（5 分钟）

1. pytest 收集测试文件的命名规则是什么？
2. 如何只运行名字里含 `login` 的测试？
3. `-x` 和 `--maxfail=3` 的区别？
4. 为什么测试用例之间不应有先后依赖？
5. 运行 `py312 -m pytest --collect-only` 能看到什么？

> 答案在本章正文中都能找到，先自己回想，再看前面的表格。

---

## 本章小结

- 测试 = 对代码行为的自动化验证，pytest 是最流行的 Python 测试框架；
- 三条铁律：文件名 `test_` 开头、函数名 `test_` 开头、用 `assert` 断言；
- 掌握常用命令行参数，能显著提升效率；
- 下一章：断言的艺术 —— `pytest.raises`、浮点比较、集合断言。
