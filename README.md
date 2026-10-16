# pytest 学习计划（Python 基础 → 测试达人）

> 适用对象：已学完 Python 基础（变量/函数/类/异常/文件读写）
> 环境：`G:\Python312`（Python 3.12.10）+ pytest 9.1.1 及全套插件
> 总时长：约 14 天（每天 1~2 小时，可按需压缩/拉伸）

---

## 一、目录结构

```
pytest/                        ← 本套材料根目录（G:\QA2\pytest）
├── README.md                     ← 本文件（学习路线图）
├── requirements.txt              ← 依赖清单
├── pytest.ini                    ← 配置示例（模板）
├── docs/                         ← 学习文档（按顺序阅读）
│   ├── 01_测试思维与pytest入门.md
│   ├── 02_断言的艺术.md
│   ├── 03_fixture夹具系统.md
│   ├── 04_参数化与标记.md
│   ├── 05_插件与工程化.md
│   └── 06_实战与TDD.md
├── cases/                        ← 经典案例（6 组，可直接运行）
│   ├── math_utils/               ← 纯函数 + 断言 + 参数化 + 异常
│   ├── string_utils/             ← 字符串 + 参数化（ids）
│   ├── file_manager/             ← tmp_path + 文件读写 + monkeypatch
│   ├── shopping_cart/            ← 类测试 + fixture 依赖
│   ├── user_service/             ← mock 数据库/邮件/随机数/时间
│   └── date_utils/               ← 参数化 + xfail + 边界
└── exercises/                    ← 练习案例（5 组，从易到难）
    ├── exercise_01_bank_account/ ← ★ 基础断言与异常
    ├── exercise_02_todo_list/    ← ★★ fixture 与 tmp_path
    ├── exercise_03_temperature/  ← ★★ 参数化专项
    ├── exercise_04_guess_game/   ← ★★★ mock 随机数与输入
    └── exercise_05_library/      ← ★★★★ 综合 TDD 毕业项目
```

每个练习目录包含：`README.md`（题目）、骨架代码（你来实现）、`solution/`（参考答案，最后再打开）。

---

## 二、14 天学习路线

| 天 | 内容 | 材料 | 产出/检查 |
| --- | --- | --- | --- |
| D1 | 测试思维 + pytest 入门 | 文档 01 | 跑通第一个测试 |
| D2 | 断言的艺术 | 文档 02 + `cases/math_utils` | 读懂并运行案例 1 |
| D3 | 断言强化 | 练习 1（银行账户） | 自己写完，再对答案 |
| D4 | fixture 基础（yield/scope） | 文档 03 | 理解注入机制 |
| D5 | conftest + 内置 fixture | `cases/file_manager` | 读懂案例 3 |
| D6 | fixture 强化 | 练习 2（待办清单） | 自己写完，再对答案 |
| D7 | 参数化与标记 | 文档 04 + `cases/string_utils` | 读懂案例 2 |
| D8 | 参数化强化 | 练习 3（温度转换） | 全部用 parametrize 写 |
| D9 | 插件：cov / html / mocker / xdist | 文档 05 + `cases/user_service` | 读懂案例 5 |
| D10 | mock 强化 | 练习 4（猜数字） | 自己写完，再对答案 |
| D11 | TDD 方法论 | 文档 06 + `cases/shopping_cart` | 读懂案例 4 |
| D12 | 综合实战 | 练习 5（图书馆）第 1 天：写测试 | 红→绿循环 |
| D13 | 综合实战 | 练习 5 第 2 天：实现 + 覆盖率 | `--cov` 达标 |
| D14 | 复盘 | 重跑全部案例 + 自测题 | 全部绿 + 完成自测 |

> 压缩方案（1 周）：跳过 D11 方法论，练习 5 直接做；每天 3 小时。
> 拉伸方案（1 个月）：每个案例用 TDD 重写一遍，对照参考答案找差距。

---

## 三、如何运行

```powershell
# 1. 运行某个经典案例
cd "G:\QA2\pytest\cases\math_utils"
py312 -m pytest -v

# 2. 运行全部经典案例
cd "G:\QA2\pytest\cases"
py312 -m pytest -v

# 3. 运行练习的参考答案（检验"标准答案"本身）
cd "G:\QA2\pytest\exercises\exercise_01_bank_account\solution"
py312 -m pytest -v

# 4. 带覆盖率运行（案例 5、练习 5 会用到）
cd "G:\QA2\pytest\cases\user_service"
py312 -m pytest --cov=user_service --cov-report=term-missing

# 5. 生成 HTML 报告
py312 -m pytest --html=report.html
```

> `py312` 是 `G:\Python312\python.exe` 的 PowerShell 别名（`Set-Alias py312 "G:\Python312\python.exe"`）。
> 如果没设置别名，用 `& "G:\Python312\python.exe" -m pytest ...`。

### ⚠️ 运行注意事项

- **练习骨架目录（exercises/*/ 根目录）是"待你实现"的状态**：骨架代码里故意留了
  `NotImplementedError`，此时直接跑骨架测试会失败——这是正常的（TDD 的"红"阶段）。
  完成实现后测试才会变绿。
- **不要在 `G:\QA2\pytest` 根目录一键跑全部**（会收集未完成的骨架）。按上面方式
  进入 `cases/` 或 `solution/` 目录运行。
- 参考实现的正确运行入口是每个练习的 `solution/` 子目录。

---

## 四、学习方法建议

1. **先读文档，再跑案例，最后做练习**——顺序不要反；
2. 经典案例的测试文件**逐行读懂**后再运行，运行前先猜输出；
3. 练习先自己写（先实现、再写测试，或严格按 TDD），**实在卡住再看 solution**；
4. 每个练习做完，用 `--cov` 检查覆盖率，目标 ≥ 90%；
5. 练习 5 是毕业项目，建议分两天完成，享受"红→绿"的完整过程；
6. 遇到报错，先读 pytest 输出的失败信息（它会告诉你实际值和期望值）。

---

## 五、环境信息（2026-10-10 配置）

| 组件 | 版本 | 路径 |
| --- | --- | --- |
| Python | 3.12.10 | `G:\Python312\python.exe` |
| pytest | 9.1.1 | G 盘 Python 自带 |
| pytest-cov | 7.1.0 | 覆盖率 |
| pytest-html | 4.2.0 | HTML 报告 |
| pytest-mock | 3.16.0 | mocker fixture |
| pytest-xdist | 3.8.0 | 并行 `-n auto` |
| pytest-timeout | 2.5.0 | 超时 |
| pytest-ordering | 0.6 | 顺序 |
| pytest-sugar | 1.1.1 | 美化输出 |

---

祝学习愉快！写完练习 5 的那天，你已经掌握 pytest 90% 的日常能力。
