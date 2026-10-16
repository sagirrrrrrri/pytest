# 第 3 章 Fixture 夹具系统

> 本章用时：约 2 小时（pytest 核心中的核心，值得多花时间）。
> 核心收获：用 fixture 优雅地管理"测试前的准备"与"测试后的清理"。

---

## 3.1 为什么需要 fixture

假设要测试一个操作数据库的函数：每个测试前要**创建连接、插入数据**，测试后要**清理数据、关闭连接**。如果每个测试都重复写这些代码，又丑又容易漏。

fixture 解决三件事：

1. **准备**：提供测试需要的数据/对象（如临时文件、数据库连接、登录用户）；
2. **清理**：测试结束后自动释放资源（删文件、关连接、清缓存）；
3. **复用**：多个测试、多个文件共享同一套准备逻辑。

---

## 3.2 第一个 fixture

```python
import pytest


@pytest.fixture
def sample_data():
    """准备一份示例数据，测试函数通过参数名自动拿到"""
    return {"name": "小明", "age": 18, "scores": [90, 85, 92]}


def test_average(sample_data):
    scores = sample_data["scores"]
    assert sum(scores) / len(scores) == pytest.approx(89)
```

关键点：

- `@pytest.fixture` 装饰的函数就是 fixture；
- 测试函数的**参数名**与 fixture 函数名一致时，pytest 自动注入；
- fixture 函数 `return` 的值就是测试拿到的值。

---

## 3.3 清理：yield 版 fixture

fixture 里用 `yield` 把"准备"和"清理"分开：`yield` 之前是准备，`yield` 之后是清理（测试全部跑完后执行）：

```python
import os
import pytest


@pytest.fixture
def temp_file(tmp_path):
    """创建一个临时文件，测试结束自动清理（tmp_path 自带清理）"""
    f = tmp_path / "data.txt"
    f.write_text("hello", encoding="utf-8")
    yield f
    # 清理代码写在这里（本例 tmp_path 会自动删除，无需手动）


def test_read_file(temp_file):
    assert temp_file.read_text(encoding="utf-8") == "hello"
```

> 注意：`yield` 后如果有代码，会在**每个使用该 fixture 的测试结束后**执行——即使测试失败也会执行（类似 finally）。

---

## 3.4 作用域：scope

fixture 默认 `scope="function"`：每个测试函数各自执行一次准备+清理。

| scope | 生命周期 | 适用场景 |
| --- | --- | --- |
| `function`（默认） | 每个测试函数一次 | 大多数情况 |
| `class` | 每个测试类一次 | 类内共享 |
| `module` | 每个模块一次 | 模块级共享（如数据库连接） |
| `session` | 整个测试会话一次 | 全局共享（如启动一次服务） |

```python
import pytest


@pytest.fixture(scope="session")
def db_connection():
    print("\n[会话级] 建立数据库连接（只建一次）")
    conn = {"connected": True, "data": []}
    yield conn
    print("\n[会话级] 关闭连接")


def test_one(db_connection):
    assert db_connection["connected"]


def test_two(db_connection):
    assert db_connection["connected"]
```

运行 `-s` 可看到"建立连接"只打印一次。

---

## 3.5 conftest.py：跨文件共享

`conftest.py` 是 pytest 的"配置 + 共享 fixture"文件，放在目录里，该目录及**子目录**的所有测试都能用里面的 fixture，**不需要 import**。

```
项目/
├── conftest.py          # 定义 login_user、db 等共享 fixture
├── test_order.py
└── sub/
    └── test_pay.py      # 也能用 conftest.py 里的 fixture
```

```python
# conftest.py
import pytest


@pytest.fixture
def login_user():
    """模拟一个已登录用户（所有模块共享）"""
    return {"username": "tester", "token": "fake-token-123", "role": "user"}
```

conftest.py 里也可以放**钩子函数**（后续章节提到）和自定义命令行选项。它是 pytest 工程化的关键文件。

---

## 3.6 内置 fixture（高频）

| fixture | 作用 | 示例 |
| --- | --- | --- |
| `tmp_path` | 每个测试独立的临时目录（`pathlib.Path`），自动清理 | 文件读写测试 |
| `tmp_path_factory` | session 级临时目录工厂 | 需要跨测试保留场景 |
| `monkeypatch` | 运行时替换对象/属性/环境变量，测试后自动还原 | mock 外部依赖 |
| `capsys` | 捕获 stdout/stderr 输出 | 测试 print 类函数 |
| `cache` | 跨测试缓存数据 | 记录上次失败的用例等 |
| `recwarn` | 收集测试中产生的警告 | 配合 warns |

**tmp_path 示例**：

```python
def test_write_and_read(tmp_path):
    target = tmp_path / "out.txt"          # 每个测试目录都不同
    target.write_text("内容", encoding="utf-8")
    assert target.read_text(encoding="utf-8") == "内容"
```

**capsys 示例**（测试打印输出）：

```python
def greet(name):
    print(f"你好，{name}！")
    return f"你好，{name}！"


def test_greet_output(capsys):
    greet("小玉")
    captured = capsys.readouterr()
    assert "你好，小玉！" in captured.out
```

**monkeypatch 示例**（替换模块属性 / 环境变量）：

```python
import os


def test_env(monkeypatch):
    monkeypatch.setenv("APP_MODE", "test")
    assert os.environ["APP_MODE"] == "test"
    monkeypatch.delenv("APP_MODE", raising=False)


def test_replace(monkeypatch):
    # 把 os.path.exists 替换成永远返回 False
    monkeypatch.setattr("os.path.exists", lambda p: False)
    assert not os.path.exists("随便什么路径")
```

---

## 3.7 fixture 依赖与工厂

**fixture 依赖 fixture**：直接声明参数即可，pytest 会自动按依赖顺序准备。

```python
@pytest.fixture
def user(login_user):
    """在 login_user 基础上加工"""
    user = dict(login_user)
    user["balance"] = 100
    return user


def test_user_balance(user):
    assert user["balance"] == 100
    assert user["token"] == "fake-token-123"   # 来自上层 fixture
```

**工厂模式（返回函数）**：当准备逻辑需要参数时，fixture 返回一个"工厂函数"：

```python
import pytest


@pytest.fixture
def make_user():
    """返回一个可以定制用户的工厂"""
    created = []

    def _factory(name="匿名用户", age=0):
        user = {"name": name, "age": age}
        created.append(user)   # 顺便记录创建过哪些
        return user

    yield _factory
    print(f"共创建了 {len(created)} 个用户")


def test_make_user(make_user):
    u1 = make_user("小明", 18)
    u2 = make_user()
    assert u1["name"] == "小明"
    assert u2["name"] == "匿名用户"
```

---

## 3.8 fixture 参数化：params
同一个 fixture 提供多组数据，每组数据产生一个用例：

```python
import pytest


@pytest.fixture(params=[("admin", True), ("guest", False), ("banned", False)])
def access_check(request):
    role, can_access = request.param
    return role, can_access


def test_access(access_check):
    role, allowed = access_check
    assert isinstance(role, str)
    assert isinstance(allowed, bool)
```

`request.param` 是拿到当前参数的关键。运行时会看到 3 个用例。

---

## 3.9 常见坑

1. **fixture 名称与测试参数名不一致** → pytest 报"缺少 fixture"错误（fixture 未定义）。
2. **忘记 yield 导致清理代码不执行**：要清理就写 `yield` 形式。
3. **scope 滥用**：session 级 fixture 会跨测试共享状态，容易产生"测试间耦合"，尽量默认 function。
4. **conftest.py 里放执行逻辑**：conftest 只应放 fixture 与配置，别放顶层执行代码。
5. **同名 fixture 冲突**：局部文件里的 fixture 会覆盖 conftest 里的同名 fixture，注意命名唯一性。

---

## 3.10 自测题

1. fixture 默认作用域是什么？改成 session 级怎么写？
2. `yield` 之前的代码和之后的代码分别在什么时候执行？
3. 如何让两个测试文件共享同一个 fixture？放在哪个文件？
4. 测试文件读写应该用哪个内置 fixture？它什么时候被清理？
5. 工厂模式 fixture 和普通 fixture 的区别是什么？什么场景用工厂？

---

## 本章小结

- fixture = 测试的"准备 + 清理"，通过参数名自动注入；
- `yield` 分隔准备与清理；`scope` 控制生命周期；
- `conftest.py` 实现跨文件共享；
- 高频内置 fixture：`tmp_path`、`monkeypatch`、`capsys`；
- 下一章：参数化与标记 —— 一份测试逻辑跑多组数据。
