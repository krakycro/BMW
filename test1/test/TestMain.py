#!python2

import sys
import os

from src.core.libPepPars import *
from src.core.libPepGen import *

##############################################################################

dir_test_folder = "./"

str_type        = ".txt"
str_start       = "_test"
str_end         = "_valid"

##############################################################################
class args:
    max_lenght = 78
    force_vertical = False


##############################################################################
# opens .py selected files
def fct_load_files(str_target):
    return \
        [(str_root, str_file)
         for (str_root, lst_dirs, lst_files) 
         in os.walk(str_target, topdown=False)
         for str_file in lst_files
         if str_file.endswith(str_start + str_type)
         ]

##############################################################################
def goAssert():
    try:
        assert False 
    except:
        pass #assert False 
    
    return True 

##############################################################################
print("==> START")

int_fail = 0
obj_args = args()
obj_dir = fct_load_files(dir_test_folder)

if len(obj_dir) == 0:
    print("    == Test Error: Empty folder!")
    int_fail = goAssert()

if not int_fail:
    for obj_file in obj_dir:
        bin_fail_case = False
        
        print("-"*30)
        print("File: ", obj_file[1])
        
        lst_file = obj_file[1].split("_")
        obj_file_core = lst_file[0]
        
        if not os.path.exists(os.path.join(obj_file[0], obj_file_core + str_end + str_type)):
            print("    == Test Error: Wrong solution file")
            bin_fail_case = goAssert()

        if not bin_fail_case:
            with open(os.path.join(obj_file[0], obj_file[1]), "r") as ftest:
                obj_pars_code = fct_parser(ftest, cls_bundle())
                obj_gen_code = fct_generator(obj_args, obj_pars_code)

                with open(os.path.join(obj_file[0],
                    obj_file_core + str_end + str_type), "r") as fvalid:
                    obj_valid = fvalid.read()
 
                    for i in range(len(obj_gen_code)):
                        #print(obj_valid[i], obj_gen_code[i])
                        if not (obj_valid[i] == obj_gen_code[i]):
                            print("    == Test Error: Not equal!") 
                            bin_fail_case = goAssert()
                            break
        
        print("Validation: ", "FAIL!" if bin_fail_case else "PASS!")
        int_fail += bin_fail_case

print("-"*30)
print("Tests:", len(obj_dir), ", Failed:", int_fail)
print("-"*30)
print("==> END")

exit(int_fail)
   
##############################################################################
##############################################################################
