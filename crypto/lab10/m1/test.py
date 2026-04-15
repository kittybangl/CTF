p = 2**127 - 1
a = 1194892878798534792121531384081377458
b = 15
h = 67197948820988379845731191820822787065
def f(K):
    return (K**3 + a * K**2 + b * K) % p - h

def f_prime(K):
    return (3 * K**2 + 2 * a * K + b) % p

def newton_raphson(K):
    while True:
        delta = f(K) * pow(f_prime(K), -1, p)
        print(delta)
        K -= delta
        if abs(delta) < 1:
            break
    return K % p

K = newton_raphson(0)