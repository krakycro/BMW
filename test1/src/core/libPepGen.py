#!python2

import re
from src.core.libPepData import *
from src.core.libPepPars import cls_bundle

##############################################################################

# regex objects
re_bracket_close = re.compile(r"\A[}\])]\Z")
re_bracket_open = re.compile(r"\A[\[{(]\Z")
re_operator = re.compile(r"\A([+*^&~|<>!/=-]{1,2})\Z")
re_op_lower = re.compile(r"\A([+-])\Z")
re_op_upper = re.compile(r"\A([*/^])\Z")
re_comment = re.compile(r"\A([#])")

##############################################################################
# parses line from lst_group into string
def fct_liner(obj_args, obj_bund, lst_line, str_lvl="", bit_body=False):
    # variables
    str_line = ""
    bit_first = True
    int_prezagr = -1
    int_zagr = 0
    int_funct = 0
    lst_prior = [-1, True]
    int_break = 0
    int_preequal = -1
    int_equal = -1
    bit_preend = False
    int_size = 0
    int_premlcomm = [0, True]
        
    ## prepare start of empty head
    if (not bit_body and len(lst_line) == 0 
            and obj_bund.str_name in LST_EMPTYTAGS):
        str_line += str_lvl
        str_line += obj_bund.str_name
        str_line += ":\n" 
        #str_line += str_lvl
        
    if len(lst_line) < 1:
        return str_line 
        
    # prepare start of head
    if not bit_body:
        str_line += str_lvl
        str_line += obj_bund.str_name
        if obj_bund.str_name != "print":
            str_line += " "
            
    # prepare start of the rest     
    elif obj_bund.str_name != "root":
        str_line += str_lvl
 
    # lists through line group and prepares for string making
    for i, x in enumerate(lst_line):
        if lst_line[i] == "=": 
            int_preequal = i
            
        if lst_line[i] == "print":
            int_preequal = i + 2
            
        #counts bracket
        if re_bracket_close.match( lst_line[i]):
            int_prezagr -= 1
            
        if re_bracket_open.match(lst_line[i]):
            if int_prezagr < 0:
                int_prezagr = 0
                
            int_prezagr += 1
        
        if lst_line[i] == '"' or lst_line[i] == "'":
            if BIT_DEBUG_GEN: print ("..", "fct_string, mlcomm?")
            int_premlcomm[0] += 1
            if int_premlcomm[0] == 3:
                int_premlcomm[0] = 0
                int_premlcomm[1] ^= True
                if BIT_DEBUG_GEN: print ("..",
                            "fct_string, mlcomm!", int_premlcomm[1])
        else:
            int_premlcomm[0] = 0
            
        # counts lowest priority
        if re_op_upper.match(lst_line[i]):
            if lst_prior[0] < 0:
                lst_prior[0] = 0
                
            if lst_prior[0] == 1:
                lst_prior[0] = 2
                
        if re_op_lower.match(lst_line[i]):
            if lst_prior[0] < 0:
                lst_prior[0] = 1
                
            if lst_prior[0] == 0:
                lst_prior[0] = 2
                
        # finds tuples and creates brackets ( )
        if (int_preequal > -1 
                and (lst_line[i] == "," 
                or lst_line[i-1] == "print") 
                and int_prezagr == -1):
            if lst_line[i] == ",":
                int_preequal = i
                
            if BIT_DEBUG_GEN: print (">>", "false tuple")
            lst_line.insert(int_preequal-1, "(")
            lst_line.append(")")
            int_preequal = -1
            
        if int_prezagr == 0:
            int_prezagr = -1
        
        # if > max, breaks # or string
        if (re.match(r"\A(r?[\"'#])",lst_line[i])
                and (len(str_lvl + STR_LVL*2)) + len(lst_line[i]) 
                    > obj_args.max_lenght):
            if re.match(r"\A(r[\"'])",lst_line[i]):
                continue
            
            l = i
            bit_str_br_end = False
            int_str_br_st = 1
            int_str_br_en = obj_args.max_lenght - (len(str_lvl + STR_LVL*2))
            if BIT_DEBUG_GEN: print (">>", "break", l)
            while 0 < int_str_br_en <= len(lst_line[l]):
                if re.match(r"\A([#])",lst_line[l]):
                        lst_line.insert(l, lst_line[l][0] 
                                + lst_line[l][int_str_br_st:int_str_br_en] 
                                + "\n")
                
                elif int_str_br_en == len(lst_line[l]):
                    lst_line.insert(l, lst_line[l][0] 
                                + lst_line[l][int_str_br_st:int_str_br_en])
                else:
                    lst_line.insert(l, lst_line[l][0] 
                            + lst_line[l][int_str_br_st:int_str_br_en]
                            + lst_line[l][0])
                
                l += 1
                int_str_br_st = int_str_br_en
                int_str_br_en += obj_args.max_lenght \
                                 - (len(str_lvl + STR_LVL) + 2)
                if BIT_DEBUG_GEN: print (">>1",
                                        (len(str_lvl + STR_LVL*2)), "-", l)
                if bit_str_br_end:
                    break
                    
                if int_str_br_en > len(lst_line[l]):
                    if BIT_DEBUG_GEN: print (">>2","end")
                    bit_str_br_end = True
                    int_str_br_en = len(lst_line[l])
                if BIT_DEBUG_GEN: print (">>2", lst_line[l-1], "-", )
            
            lst_line.pop(l)
            i = l - 1
            
        int_size += len(lst_line[i]) + 1   
        #if BIT_DEBUG_GEN: print ">>", "end", i
    ##
    
    ##
    # lists through line group and makes a string
    for i, x in enumerate(lst_line):
        # sets (=) flag for returning result to a variable
        if int_equal == -1 and int_funct < 1 and lst_line[i] == "=":
            if BIT_DEBUG_GEN: print (">>", "int_equal = ")
            int_equal = len(str_line) + 3
            
        # generates vertical list
        if (obj_args.force_vertical
                and (lst_line[i] in LST_PAR_CON
                or lst_line[i] in LST_GEN_CON
                or re.match(r"\A([,+-])\Z", lst_line[i]))
                and int_equal > 0 and int_zagr % 2 != 0):
            if BIT_DEBUG_GEN: print (">>", "vertical lst_group")
            if lst_line[i] == ",":
                str_line += ", "
                
            if ((lst_line[i] == lst_line[-1]
                or not re_comment.match(lst_line[i+1]))
                    and lst_prior[1]):
                str_line += "\n"
                str_line += str_lvl + STR_LVL*(int_zagr)
                int_break = len(str_line)
            
            if lst_line[i] == ",":
                continue
                
        # generates a # comment
        if re_comment.match(lst_line[i]):
            if BIT_DEBUG_GEN: print (">>", "# comment")
            if lst_line[i] != lst_line[0]:
                str_line += STR_LVL + "\t"
                str_line += lst_line[i]
                if lst_line[i] != lst_line[-1]:
                    str_line += "\n"
                if not obj_args.force_vertical:
                    str_line += str_lvl + STR_LVL*(int_zagr)
                    
            else:
                str_line += lst_line[i]
                
            if obj_args.force_vertical and (int_equal == -1
                    or (lst_line[i] != lst_line[-1] 
                    and not re_bracket_close.match(lst_line[i+1]))):
                str_line += str_lvl + STR_LVL*(int_zagr)
                
            int_break = len(str_line)
            continue
            
        # generates a max lvl break
        if (lst_line[i] != lst_line[0] 
                and not re.match(r"\A([r\"':,(\\n)\]} ]\Z)", lst_line[i])
                and len(str_line) + len(lst_line[i]) 
                    > obj_args.max_lenght + int_break):
            if BIT_DEBUG_GEN: print (">>", "Max break")
            if re_operator.match(lst_line[i-1]):
                str_line = str_line[:-2]
                
            if int_zagr == 0 and re.match(r"\A([\"]} ]\Z)", lst_line[i-1]):
                str_line += "\\" 
                
            if int_equal == -1 \
                    or (lst_line[i] != lst_line[-1] 
                    and not re_bracket_close.match(lst_line[i+1])):
                str_line += "\n"
                if int_funct > 0:
                    str_line += " "*(int_funct)
                    
                else:
                    str_line += str_lvl + STR_LVL*2
                    
            lst_prior[1] = True
            if (re_operator.match(lst_line[i-1]) 
                    and int_funct < 1):
                str_line += " " + lst_line[i-1] + " "
                
            int_break = len(str_line)
            
        # generates an empty head line  
        if obj_bund.str_name in LST_ONEITEMS:
            if BIT_DEBUG_GEN: print (">>", "import itd.")
            if not bit_first and lst_line[i] != ",":
                str_line += "\n" + str_lvl + obj_bund.str_name \
                            + " " + lst_line[i]
                bit_first = False
                continue
                
            if lst_line[i] == ",":
                continue
                
        bit_first = False
        
        # sets priority of operants
        if re_op_upper.match(lst_line[i]):
            if lst_prior[0] > 1:    
                lst_prior[1] = False
                
        if re_op_lower.match(lst_line[i]):
            if lst_prior[0] > 1:  
                lst_prior[1] = True
        
        ## adds text to string:        
        # adds equualization 
        if (lst_line in obj_bund.lst_head and int_zagr > 0 
                and re.match(r"\A([=])\Z", lst_line[i])):
            if BIT_DEBUG_GEN: print (">>", "add =")
            str_line += lst_line[i]
            continue
        
        # adds text
        if (lst_line[i] in LST_PAR_CON or lst_line[i] in LST_GEN_CON):
            if BIT_DEBUG_GEN: print (">>", "add text")
            if obj_args.force_vertical and int_equal > 0:
                str_line += lst_line[i] + " "
            else:
                str_line += " " + lst_line[i] + " "
                
            continue
        
        # adds operation    
        if (re_operator.match(lst_line[i])):
            if BIT_DEBUG_GEN: print (">>", "add sign")
            if ((int_equal == 0 or lst_prior[1])
                    and (not re_bracket_open.match(lst_line[i-1]))):
                str_line += " " + lst_line[i] + " "
            else:
                str_line += lst_line[i]
                
            continue
        
        # adds ", " if no bracket
        if (re.match(r"\A([,]|not)", lst_line[i])
                #and lst_line[i] != "print" 
                and (lst_line[i] == lst_line[-1]
                or not re_bracket_close.match(lst_line[i+1]))):
            if BIT_DEBUG_GEN: print (">>", "add ,")
            str_line += lst_line[i] + " "
            continue
        
        # adds ": " if no bracket ]   
        if (re.match(r"\A([:])", lst_line[i])
                and (lst_line[i+1] == lst_line[-1]
                or not re.match(r"\A[\]]\Z", lst_line[i+2]))):
            if BIT_DEBUG_GEN: print (">>", "add :")
            str_line += lst_line[i] + " "
            continue
        ##
        
        # makes neline before bracket if vertical
        if (obj_args.force_vertical 
                and int_equal > 0 and int_zagr % 2 != 0 
                and re_bracket_close.match(lst_line[i])
                and not re_bracket_open.match(lst_line[i-1])):
            if BIT_DEBUG_GEN: print (">>", "close )")
            if not re_comment.match(lst_line[i - 1]):
                str_line += "\n"
                
            str_line += str_lvl + STR_LVL*(int_zagr - 1)
            int_break = len(str_line)
        
        # default write
        str_line += lst_line[i]
        
        ## counts brackets
        if re_bracket_close.match(lst_line[i]):
            if BIT_DEBUG_GEN: print (">>","int_zagr ne")
            int_zagr -= 1
            if int_zagr == 0:
                int_funct = 0
                #int_equal = -1
                
        if re_bracket_open.match(lst_line[i]):
            if BIT_DEBUG_GEN: print (">>", "int_zagr da")
            if int_zagr == 0 and re.match(r"\A[\w]", lst_line[i - 1]):
                if BIT_DEBUG_GEN: print (">>", "int_funct!")
                int_funct = len(str_line)
                
            int_zagr += 1
        ##
        
        # makes neline after bracket if vertical
        if (obj_args.force_vertical 
                and int_equal > 0 and int_zagr % 2 != 0 
                and re_bracket_open.match(lst_line[i])
                and not re_bracket_close.match(lst_line[i + 1])):
            if BIT_DEBUG_GEN: print (">>", "open (")
            str_line += "\n"
            str_line += str_lvl + STR_LVL*(int_zagr)
            int_break = len(str_line)
    ##
    
    # ends line + adds : if head
    if lst_line not in obj_bund.lst_head:
            str_line += "\n"
        
    elif obj_bund.str_name not in LST_INLINERS: 
        str_line += ":\n"
        
    else: 
        str_line += " "
    
    if BIT_DEBUG_GEN: print (">>", obj_bund.str_name, "fct_liner", str_line)
    return str_line
    
##############################################################################
# merges lines or new bundle instance to current string
def fct_merger(obj_args, obj_bund, lst_group, str_lvl="", bit_body=False):
    str_group = ""
    # lists through bundle items
    for i, x in enumerate(lst_group):
        # nakes another bundle instance and adds it as group
        if isinstance(lst_group[i], cls_bundle):
            if BIT_DEBUG_GEN: print (">>", "obj_bund", lst_group[i].str_name)
            str_group += fct_generator(obj_args, lst_group[i], str_lvl)
        
        # makes a line of text
        else:
            if BIT_DEBUG_GEN: print (">>", "lst_group", lst_group[i])
            str_group += fct_liner(obj_args, obj_bund, lst_group[i], 
                                   str_lvl, bit_body)
    
    return str_group
    
##############################################################################  
# main generator of python text (recursive), returns a string
def fct_generator(obj_args, obj_bund, str_lvl=""):
    str_chunk = ""
    inln = True if obj_bund.str_name in LST_INLINERS else False
    
    # generating bit_body of root/bit_first instance
    if obj_bund.str_name == "root":
        if BIT_DEBUG_GEN: print (">>", "root")
        return fct_merger(obj_args, obj_bund, obj_bund.lst_body, 
                          str_lvl, True)
        
    # generating head of current bundle
    if BIT_DEBUG_GEN: print (">>", "head", obj_bund.str_name)
    str_chunk += fct_merger(obj_args, obj_bund, obj_bund.lst_head, str_lvl)
    
    # generating bit_body of current bundle
    if BIT_DEBUG_GEN: print (">>", "bit_body", obj_bund.str_name)
    str_chunk += fct_merger(obj_args, obj_bund, obj_bund.lst_body, 
                            str_lvl + STR_LVL, True)
    
    # finishes a group witn a newline
    if len(str_chunk) > 0:
        while str_chunk[-1] == "\n":
            str_chunk = str_chunk[:-1]
            
    if not inln:
        str_chunk += "\n"  
        
    str_chunk += "\n"    
    if obj_bund.str_name == "class":
        str_chunk += "\n" 
    
    return str_chunk
    
##############################################################################
##############################################################################
