# CryptoHack - Hamiltonicity 1 解题

## 漏洞本质

题目把 Fiat-Shamir challenge bit 设为：

- 先提交承诺矩阵 `A`
- 再计算 `challenge = H(params || FS_state || A)[-1] & 1`

由于 `A` 的 Pedersen 承诺本身含随机数，攻击者可以反复重采样 `A`，直到哈希出来的 bit 命中自己想要的分支（期望约 2 次命中一次）。

## 两个可用分支

- `e=0`：提交“坏图 `G` 的置换”及完整 opening（这是合法证明）。
- `e=1`：提交“另一张有 Hamilton 环的图”的承诺，只打开环边（verifier 只检查 `A` 内部环边可开为 1，不检查与原始 `G` 的一致性）。

因此攻击者可逐轮强制 challenge 位并总是给出对应可验证回答，最终通过全部轮次。

## 代码说明

`solve_hamiltonicity1.py` 提供两种模式：

1. `--mode local`（默认）
   - 内置 verifier 逻辑，自测每轮 forged proof 都可通过。
2. `--mode remote`
   - 连接远端服务并逐轮发送 `{"A":...,"z":...}`。

## 用法

### 本地自测

```bash
python -u solve_hamiltonicity1.py --mode local --rounds 128
```

### 远端获取 flag

```bash
python -u solve_hamiltonicity1.py --mode remote --host archive.cryptohack.org --port 3721 --rounds 128
```

> 如果你环境可出网，这条命令会在通过 128 轮后打印服务返回内容（通常含 flag）。
