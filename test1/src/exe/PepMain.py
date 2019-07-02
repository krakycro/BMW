#!python2

import sys
import os
import argparse
from src.core.libPepPars import *
from src.core.libPepGen import *

##############################################################################
# opens .py selected files
def fct_load_files(str_target):
    return \
        [(str_root, str_file)
         for (str_root, lst_dirs, lst_files) 
         in os.walk(str_target, topdown=False)
         for str_file in lst_files
         if str_file.endswith(".py")
         ]

##############################################################################
# start/main point for parser
obj_parser = argparse.ArgumentParser(description="Python PEP8 parser")
obj_parser.add_argument("-o", "--dir_open",         
                        help="Directory for parsing",               
                        required=True,
                        type=str)
obj_parser.add_argument("-s", "--dir_save",         
                        help="Directory for saving",                
                        required=False,
                        type=str)
obj_parser.add_argument("-v", "--force_vertical",   
                        help="Force of vertical listing",         
                        required=False,
                        type=bool,
                        default=False)
obj_parser.add_argument("-l", "--max_lenght",       
                        help="Using different max lenth than 79",   
                        required=False, 
                        default=78,
                        type=int)                        
obj_args = obj_parser.parse_args()

obj_dir = fct_load_files(obj_args.dir_open)

# first parses data from file and then generates new file
print ">>> START"
for obj_file in obj_dir:
        print obj_file[1]
        with open(os.path.join(obj_file[0], obj_file[1]), "r") as f:
            obj_pars_code = fct_parser(f, cls_bundle())
            if BIT_DEBUG_PAR: print obj_pars_code
            
            obj_gen_code = fct_generator(obj_args, obj_pars_code)
            if BIT_DEBUG_GEN: print obj_gen_code
            
            if not os.path.exists(obj_args.dir_save):
                os.makedirs(obj_args.dir_save)
            
            with open(os.path.join(obj_args.dir_save,
                      obj_file[0][5:], obj_file[1]), "w") as f:
                f.write(obj_gen_code)
            
print "<<< END"

##############################################################################
##############################################################################        
