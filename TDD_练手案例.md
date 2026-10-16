# TDD 练手案例说明（仅需求，无源码）

> 本文件提供三个由浅入深的测试驱动开发（TDD）练手案例。
> 每个案例只给出需求说明，**不提供任何源码**，请自行用 TDD 方式（先写测试 → 让它通过 → 重构）实现。
> 建议测试框架：`pytest`（你环境里已有 pytest 9.1.1）。

## 练习方法（Red-Green-Refactor）

1. **红（Red）**：先写一个会失败的测试，运行确认它失败。
2. **绿（Green）**：用最简单的代码让测试通过。
3. **重构（Refactor）**：在测试保护下整理代码，保持测试全绿。

节奏：一次只写一个测试 → 让它通过 → 再写下一个。切忌一次性写完所有测试或所有实现。

---

## 案例一：温度单位转换器（入门）

### 背景
实现一个温度转换模块，提供两个函数：摄氏转华氏、华氏转摄氏。

### 需求说明

1. **`celsius_to_fahrenheit(c)`**
   - 输入：一个数字（int 或 float），表示摄氏温度。
   - 输出：对应的华氏温度，公式 `F = C × 9/5 + 32`。
   - 允许极小的浮点误差（用 `pytest.approx` 比较）。

2. **`fahrenheit_to_celsius(f)`**
   - 输入：一个数字，表示华氏温度。
   - 输出：对应的摄氏温度，公式 `C = (F − 32) × 5/9`。

3. **边界与异常**
   - 支持负数（如 −40 度，摄氏与华氏在此相等，是很好的测试点）。
   - 输入不是数字（如字符串、`None`）时，抛出 `TypeError`。

### 建议的测试顺序（由简到难）
1. 0°C → 32°F
2. 100°C → 212°F
3. −40°C → −40°F（负数）
4. 反向转换 32°F → 0°C
5. 输入非法类型时抛 TypeError

---

## 案例二：银行账户模拟（进阶）

### 背景
实现一个 `Account` 类，模拟支持存取款、扣手续费、查询余额的简易账户。

### 需求说明

1. **开户（构造函数）**
   - `Account(owner, initial_balance=0)`
   - `owner` 必须是长度大于 0 的字符串，否则抛 `ValueError`。
   - `initial_balance` 必须 ≥ 0，否则抛 `ValueError`。

2. **存款 `deposit(amount)`**
   - `amount` 必须 > 0，否则抛 `ValueError`。
   - 存款后余额增加。

3. **取款 `withdraw(amount)`**
   - `amount` 必须 > 0，否则抛 `ValueError`。
   - 余额不足时（取出的钱超过当前余额）抛 `InsufficientFundsError`（自定义异常）。
   - 成功取款后余额减少。

4. **手续费规则**
   - 每笔取款成功时，额外扣 1 元手续费（从余额中一并扣掉）。
   - 余额判断基于"取款金额 + 手续费"：余额 5 元取 4 元允许（扣完剩 0），取 5 元不允许。

5. **查询**
   - `balance` 属性：当前余额。
   - `owner` 属性：开户人姓名。

### 建议的测试顺序
1. 开户后余额等于初始值
2. 存款后余额正确增加
3. 非法开户参数（空姓名、负数初始余额）抛 ValueError
4. 取款成功后余额减少，且扣了 1 元手续费
5. 余额不足时取款抛 InsufficientFundsError，且余额不变
6. 取 0 元或负数抛 ValueError

> 提示：自定义异常 `InsufficientFundsError(Exception)` 单独定义，方便 `pytest.raises` 精确匹配。

---

## 案例三：简易任务清单 Todo List（综合）

### 背景
实现一个 `TodoList` 类，模拟命令行任务管理工具的核心逻辑：添加、完成、列出、删除任务，并支持按状态筛选。

### 需求说明

1. **数据模型**
   - 每个任务含：`id`（自动递增整数，从 1 开始）、`title`（字符串）、`done`（布尔，默认 False）。
   - `title` 为空字符串或纯空白时，添加应抛 `ValueError`。

2. **添加 `add(title)`**
   - 返回新任务的 `id`。
   - 任务默认未完成。

3. **完成 `complete(id)`**
   - 将指定任务标记为已完成。
   - `id` 不存在时抛 `KeyError`。

4. **删除 `remove(id)`**
   - 删除指定任务，返回被删除任务的标题。
   - `id` 不存在时抛 `KeyError`。
   - 删除后 `id` 不复用（新任务继续递增，避免 id 混乱）。

5. **列出**
   - `list_all()`：返回所有任务（按 id 升序），每项为字典 `{"id":..., "title":..., "done":...}`。
   - `list_pending()`：只返回未完成任务。
   - `list_done()`：只返回已完成任务。

6. **统计**
   - `pending_count` 属性：未完成任务数量。
   - `done_count` 属性：已完成任务数量。

### 建议的测试顺序
1. 添加一个任务，返回 id 为 1，且默认未完成
2. 连续添加多个任务，id 依次递增
3. 添加空标题抛 ValueError
4. complete(1) 后该任务 done 为 True，list_done 能查到
5. complete(不存在的 id) 抛 KeyError
6. remove 后任务消失，且列表正确
7. remove 不存在的 id 抛 KeyError
8. 删除后新任务 id 继续递增（不复用）
9. pending_count / done_count 统计正确

> 提示：这个案例适合练习"用测试驱动类的设计"——先想清楚接口，再逐个用测试逼出实现。

---

## 运行环境
- Python 3.12（`G:\Python312\python.exe`）
- 测试框架：`pytest`（已安装 9.1.1）
- 运行：把测试文件命名为 `test_xxx.py`，在目录里执行 `py312 -m pytest -v`

## 建议的目录组织（每个案例一个独立目录）
```
G:\QA2\pytest\tdd_cases\
├── temperature/        # 案例一：test_temperature.py + temperature.py
├── bank_account/       # 案例二：test_bank.py + bank.py
└── todo_list/          # 案例三：test_todo.py + todo.py
```
每个目录里先建空的 `test_xxx.py`，按上面的"测试顺序"逐个写测试、逐个让实现通过。
