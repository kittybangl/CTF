# CTF 题解仓库总览

已按题型将仓库重构为两大类：

- `crypto/`：密码学相关题目、实验、课程工程
- `pwn/`：二进制利用相关题目

---

## 1. 仓库结构（按题型）

```text
.
├── README.md
├── crypto/
│   ├── solve_hamiltonicity1.py
│   ├── lab01/ ~ lab04、lab10/
│   ├── Schnorr_EUFNMA/、Schnorr_EUFCMA/
│   ├── KatzWang_EUFNMA/、DHI_DY05/
│   ├── Bleichenbacher/、dlog_cdh/、cdh_quadratic/
│   └── ...
└── pwn/
    └── baby_heap_buffer_overflow/
```

> 说明：该仓库仍然是“题解与实验集合”，不是单一构建工程。

---

## 2. Crypto 目录

`crypto/` 下放置了所有密码学相关内容，包括：

- CryptoHack 脚本与实验代码（如 `solve_hamiltonicity1.py`）
- 各 lab 目录（`lab01` - `lab04`, `lab10`）
- Java 课程工程（Schnorr、KatzWang、DHI、CDH 等）

示例命令：

```bash
# 本地验证 Hamiltonicity 1
python3 -u crypto/solve_hamiltonicity1.py --mode local --rounds 128
```

---

## 3. Pwn 目录

`pwn/` 下目前包含：

- `baby_heap_buffer_overflow/`：题目源码、二进制、利用脚本与详细分析

示例命令：

```bash
# 默认尝试读取 /flag
python3 pwn/baby_heap_buffer_overflow/solve.py
```

---

## 4. 使用建议

- 密码题：优先从 `crypto/` 下按题目目录进入。
- 二进制题：优先从 `pwn/` 下进入对应题目目录。
- 若你后续新增题目，建议继续按 `crypto/` 与 `pwn/` 分类放置，保持一致性。
