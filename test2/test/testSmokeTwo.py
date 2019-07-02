from src.libFunc import *

try:
    A = bar(1, 2)
    B = bar(1.0, 2.0)
    C = bar("1", "2")
    print("TEST step 1: PASS!")
except:
    print("TEST step 1: FAIL!")
