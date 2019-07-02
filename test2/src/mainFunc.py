import sys

from src.libFunc import *

argv = [0,0]

try:
    argv[0] = sys.argv[1]
    argv[0] = int(argv[0])
except:
    pass
try:
    argv[1] = sys.argv[2]
    argv[1] = int(argv[1])
except:
    pass

A = foo(argv[0], argv[1])
B = bar(A.x, A.y)

print(B)
