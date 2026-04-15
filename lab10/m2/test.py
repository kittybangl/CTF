p = 2**1279-1	
prime_set = []
for i in range(1279): 
    print(i)
    prime_set.append(pow(2, i, p))
print(prime_set)
print(len(prime_set))