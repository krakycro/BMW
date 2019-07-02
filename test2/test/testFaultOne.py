from src.libFunc import *

try:
    A = foo()
except:
    print("TEST step 1: PASS!")
    exit(0)

print("TEST step 1: FAIL!")
exit(1)
