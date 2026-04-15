# Schnorr_EUFNMA 模块说明

> 这是一个基于课程框架的 Java 项目，目标是实现从 **Schnorr EUF-NMA 对手** 到 **DLog 挑战** 的归约。

## 1. 目录职责

```text
Schnorr_EUFNMA/
├── lib/Schnorr_EUFNMA.jar                   # 框架依赖（挑战者、群、测试基础设施）
└── src/
    ├── basics/                              # 通用接口（adversary/reduction/challenger）
    ├── schnorr/
    │   ├── *.java                           # Schnorr 相关接口与数据结构
    │   ├── Schnorr_EUFNMA_TestRunner.java   # 本地测试入口
    │   └── reductions/
    │       ├── A_*.java                     # 抽象基类
    │       └── Schnorr_EUFNMA_Reduction.java# 学生实现
    └── utils/                               # Pair/Triple/工具函数
```

## 2. 核心对象关系

- `I_DLog_Challenger`：提供离散对数挑战 `(g, x=g^a)`，目标恢复 `a`。
- `I_Schnorr_EUFNMA_Adversary`：在随机预言机模型下尝试伪造 Schnorr 签名。
- `A_Schnorr_EUFNMA_Reduction`：归约器抽象基类，负责把上面两者“桥接”起来。
- `Schnorr_EUFNMA_Reduction`：当前仓库中的具体实现。

## 3. `Schnorr_EUFNMA_Reduction` 的实现逻辑（当前版本）

`src/schnorr/reductions/Schnorr_EUFNMA_Reduction.java` 主要做了这些事：

1. 在 `run()` 中取到 DLog challenge，设置内部 `gen` 与 `x`。
2. 用同一随机种子调用 adversary 两次，期间清空并重建 hash oracle 记录（`Sites`）。
3. 期望拿到同消息下两组不同挑战值 `(c1,s1)`、`(c2,s2)` 的可验证签名。
4. 根据 Schnorr 关系式用 `(s1-s2)/(c1-c2)` 恢复离散对数解并返回。

此外：

- `getChallenge()` 返回 `(base=gen, key=x)` 作为 Schnorr 公钥。
- `hash(message, r)` 用 `HashMap<Pair<String, IGroupElement>, BigInteger>` 模拟随机预言机的一致性回答。

## 4. 测试入口

`src/schnorr/Schnorr_EUFNMA_TestRunner.java` 会构造多组测试：

- 随机代数群参数
- 不同 adversary 类型
- 多轮统计通过率（`n` 次测试达到阈值 `t` 即 pass）

其 `main` 里默认使用：

- 128-bit 群参数
- `Schnorr_EUFNMA_Reduction.class`

## 5. 如何阅读这部分代码

推荐顺序：

1. `schnorr/Schnorr_EUFNMA_TestRunner.java`（看执行流程）
2. `schnorr/reductions/A_Schnorr_EUFNMA_Reduction.java`（看要求实现的方法）
3. `schnorr/reductions/Schnorr_EUFNMA_Reduction.java`（看当前策略）
4. `schnorr/*.java`（理解挑战者/对手接口）

## 6. 注意事项

- 这个目录依赖课程框架（jar + 额外包），并非独立 Maven/Gradle 工程。
- 若你要重跑测试，请保证课程环境中的依赖路径和 classpath 配置完整。
