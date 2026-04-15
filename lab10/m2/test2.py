g = 2
sk = 1<<22
p = 100354823939110433032730292782729054578020819028650209416946649328915946626955630648940747400874471722916780805908279452095500078825705096097895248713123261461652556064230232380883326732822588319210964177715103509578771725344399788674711708485821404292728869805214337885377280447267805993616280552969783451607
pk = pow(g, sk, p)
print(pk)

import math

def pollard_rho(p, g, pk):
    """
    使用Pollard rho算法计算离散对数。

    p: 质数
    g: 基础数
    pk: 公钥
    """

    def f(x):
        """
        定义函数 f(x) = g^x mod p
        """
        return pow(g, x, p)

    x = 2  # 初始值
    y = 2
    d = 1
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), p)

    if d == p:
        # Pollard rho算法失败，重新开始
        return pollard_rho(p, g, pk)
    else:
        # 求解 x = sk
        phi = (p - 1) // d
        pk_inv = pow(pk, phi - 1, p)
        sk = ((math.log(pk_inv) - math.log(f(x) // d)) % phi) / phi
        return int(sk)
    
print(pollard_rho(p, g, pk))