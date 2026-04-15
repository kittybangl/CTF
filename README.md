# CTF 题解仓库总览

这个仓库目前主要包含 3 块内容：

1. **CryptoHack - Hamiltonicity 1（Python）**
2. **baby_heap_buffer_overflow（Pwn，C + Python PoC）**
3. **Schnorr_EUFNMA（Java 课程项目/归约实现）**

下文按“目录逻辑 + 运行方式 + 关键点”整理，方便快速上手。

---

## 1. 仓库结构

```text
.
├── README.md                             # 本文件：全仓库导航
├── solve_hamiltonicity1.py               # CryptoHack Hamiltonicity 1 解题脚本
├── baby_heap_buffer_overflow/
│   ├── chal.c                            # 题目源码
│   ├── exe                               # 题目二进制
│   ├── solve.py                          # 本地/远程利用脚本
│   └── README.md                         # 该题详细分析
└── Schnorr_EUFNMA/
    ├── src/                              # Java 源码（接口、归约、测试器）
    ├── lib/Schnorr_EUFNMA.jar            # 课程配套 jar
    └── README.md                         # 模块逻辑说明
```

---

## 2. CryptoHack - Hamiltonicity 1（`solve_hamiltonicity1.py`）

### 2.1 核心思路

该脚本实现 **Fiat-Shamir challenge bit grinding**：

- 先构造承诺矩阵 `A`
- 计算 `bit = H(params || fs_state || A)[-1] & 1`
- 反复重采样直到 `bit` 命中自己当前能回答的分支

利用点在于题目对 `e=0/e=1` 两个分支的检查可被分别构造通过，从而逐轮伪造直至拿到最终输出。

### 2.2 两种模式

- `--mode local`：本地模拟 verifier，验证伪造逻辑。
- `--mode remote`：连接远端服务按轮交互。

### 2.3 常用命令

```bash
# 本地验证
python3 -u solve_hamiltonicity1.py --mode local --rounds 128

# 远端交互
python3 -u solve_hamiltonicity1.py --mode remote --host archive.cryptohack.org --port 3721 --rounds 128
```

---

## 3. baby_heap_buffer_overflow（`baby_heap_buffer_overflow/`）

详细分析见：[`baby_heap_buffer_overflow/README.md`](baby_heap_buffer_overflow/README.md)。

### 3.1 漏洞概述

- `content[64]` 仅 `0x40` 字节
- `fgets(..., 0x64, ...)` 可写到 `0x63` 字节 + `\0`
- 发生堆上越界，覆盖相邻 `vtable` 函数指针

### 3.2 利用概述

`solve.py` 通过改写 `vtable->write = system@plt`，随后把命令字符串写入 `object->content`，最后触发 write 分支执行命令。

### 3.3 常用命令

```bash
# 默认尝试读取 /flag
python3 baby_heap_buffer_overflow/solve.py

# 执行自定义命令
python3 baby_heap_buffer_overflow/solve.py --cmd 'id'

# 自动尝试常见 flag 路径
python3 baby_heap_buffer_overflow/solve.py --try-common-flags
```

---

## 4. Schnorr_EUFNMA（`Schnorr_EUFNMA/`）

该目录是 Java 的 Schnorr EUF-NMA 归约实现与测试工程。

- 入口测试器：`src/schnorr/Schnorr_EUFNMA_TestRunner.java`
- 主要实现：`src/schnorr/reductions/Schnorr_EUFNMA_Reduction.java`
- 接口定义位于 `src/schnorr/*.java` 与 `src/basics/*.java`

具体模块关系和逻辑梳理见：[`Schnorr_EUFNMA/README.md`](Schnorr_EUFNMA/README.md)。

---

## 5. 建议阅读顺序

1. 先看本文件了解整体布局。
2. 做 pwn 题时：看 `baby_heap_buffer_overflow/README.md` + 跑 `solve.py`。
3. 做密码题时：看 `solve_hamiltonicity1.py` 注释与 `--mode local` 输出。
4. 研究 Schnorr 归约时：看 `Schnorr_EUFNMA/README.md`，再进 `src/schnorr/reductions/`。

---

## 6. 备注

- 本仓库偏“题解与实验”性质，不是统一构建工程。
- 各目录依赖不同（Python / C / Java），建议按子目录分别运行。
