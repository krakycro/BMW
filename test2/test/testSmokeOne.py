from src.libFunc import *

try:
    A = foo(1, 2)
    B = foo(1.0, 2.0)
    C = foo("1", "2")
    print("TEST step 1: PASS!")
except:
    print("TEST step 1: FAIL!")
