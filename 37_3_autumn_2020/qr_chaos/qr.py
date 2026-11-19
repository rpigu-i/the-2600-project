# python3
# qr.py
import string
import random
N = 10
for i in range(100):
qr = ''.join(random.choices(string.ascii_uppercase +
string.ascii_lowercase, k=N))
print(qr, end='\n')
print()


