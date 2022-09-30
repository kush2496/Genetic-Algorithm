import random

import numpy as np
a=np.random.random((2,4))
print(a)
b=np.zeros((2,4))
b=a
print(b)
c=np.zeros((2,4))
for i in range (2):
    for j in range (4):
        c[i][j] = (a[i][j] - b[i][0])/(b[i][1] - b[i][0])
print(c)

