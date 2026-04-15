def power_inverse(a, b, c):
    # 求 (1/a)^b mod c
    # 求 a 对于模数 c 的乘法逆元
    a_inv = pow(a, c-2, c)
    
    # 计算 pow(a^-1, b, c)
    res = pow(a_inv, b, c)
    return res

# print(power_inverse(2, 5, 67))
print((pow(2, 2, 67) * power_inverse(3, 2, 67))%67)
print((pow(4, 2, 67) * power_inverse(6, 2, 67))%67)
# print(pow(4, 5, 6))