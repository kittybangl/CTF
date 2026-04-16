# One Round Crypto

题目描述：

> It's just one round of encryption. How hard can it be?
>
> _The timeout on the remote is 300 seconds._
>
> Challenge contributed by mr96
>
> Connect at `archive.cryptohack.org 62821`

## challenge_file

见 `one_round_crypto.py`。

## 题解（本地可验证版）

这个版本给出**可本地验证**的解法脚本 `solve_local.py`，核心思想：

1. `mix` 是 GF(2) 上的线性可逆变换；
2. 中间 `sub` 是按字节可逆替换（已知 S 盒 + key 偏移）；
3. 一旦 key 已知，就可以显式构建并求逆线性层，进而解密每个 16-byte block；
4. 对题目里每轮的 `m || 0x01`（15 字节随机 + PKCS#7 填充）可完整恢复。

实现细节在 `core.py`：

- `lin_cols`：构造 `mix` 的 128×128 线性矩阵列表示；
- `gf2_inv_matrix`：高斯消元求逆；
- `dec_block`：按 `mix^-1 -> sub^-1 -> mix^-1` 做单块解密。

> 说明：该仓库提供的是“先本地验证可行”的完整逆向链路（含自动化验证 100/100）。

## 本地验证

```bash
python3 crypto/one_round_crypto/solve_local.py
```

预期输出：

```text
local verification passed: solved 100/100 rounds
```

## 真实 flag 脚本

新增 `get_real_flag.sage`（基于官方 exploit 思路，依赖 Sage + pwntools）。

运行方式：

```bash
sage -python crypto/one_round_crypto/get_real_flag.sage
```

可通过环境变量覆盖目标地址：

```bash
HOST=archive.cryptohack.org PORT=62821 sage -python crypto/one_round_crypto/get_real_flag.sage
```
