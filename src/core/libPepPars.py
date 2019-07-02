#!python2

import re
from src.core.libPepData import *

##############################################################################


##############################################################################
# parser bundle for all shared flags and operations
class cls_bundle:    
    # variables
    str_name = None
    lst_head = None
    lst_body = None
    int_lvl = 0
    int_tree = 0
    
    # flags
    str_hist = ""
    str_retrn = ""
    lst_tab = []
    lst_str = []
    bit_comm = False
    bit_end = False
    bit_fin = False
    int_free = 0
    lst_upper = []
    int_inline = 0
    bit_newln = False
    
    ##########################################################################
    def __init__(self, _str_name=None, _int_lvl=0):
        self.int_lvl = _int_lvl
        self.str_name = _str_name
        self.lst_head = []
        self.lst_body = []
        self.lst_tab = [0, 0]
        self.lst_upper = [True, True]
        self.lst_str = [False, "", 0, False, 0, False]
    
    ########################################################################## 
    # writes bundle as a text
    def __str__(self):
        str_i_lvl = "  "*(self.int_lvl + 1)
        str_txt =  "{\n"
        str_txt += str_i_lvl*2 + "str_name:" + self.str_name + "\n"
        str_txt += str_i_lvl*2 + "lst_tab: %d\n" %(self.int_tree)
        str_txt += str_i_lvl*2 + "lst_head:\n"
        str_txt += str_i_lvl*2 + "[\n"
        for incr, x in enumerate(self.lst_head):
            str_txt += str_i_lvl*3 \
                        + (", " if incr > 0 else "  ") \
                        + x.__str__() + "\n"
                        
        str_txt += str_i_lvl*2 + "]\n"
        str_txt += str_i_lvl*2 + "lst_body:\n"
        str_txt += str_i_lvl*2 + "[\n"
        for incr, x in enumerate(self.lst_body):
            str_txt += str_i_lvl*3 \
                        + (", " if incr > 0 else "  ") \
                        + x.__str__() + "\n"
                        
        str_txt += str_i_lvl*2 + "]\n"
        str_txt += str_i_lvl + "}"
        return str_txt
    
    ##########################################################################
    # preparing new bundle
    def fct_start(self):
        if BIT_DEBUG_PAR: print ("..", "new fct_start")
        if self.str_name == None:
            self.str_name = "root"
            self.lst_upper = [False, True]
            if BIT_DEBUG_PAR: print ("..", "root!")
            
    ##########################################################################
    # parsing string chars and it's triggered events
    def fct_string(self, str_char):
        if self.bit_comm:
            return False
            
        if str_char == '"' or str_char == "'":
            if BIT_DEBUG_PAR: print ("..", "fct_string, mlcomm?")
            self.lst_str[4] += 1
            if self.lst_str[4] == 3:
                self.lst_str[4] = 0
                self.lst_str[5] ^= True
                if BIT_DEBUG_PAR: print ("..",
                            "fct_string, mlcomm!", self.lst_str[5])
        else:
            self.lst_str[4] = 0
            
        # if not string  
        if not self.lst_str[0]:                 
            # if raw string  
            if not self.lst_str[3] and str_char == "r":
                self.lst_str[3] = True
                if BIT_DEBUG_PAR: print ("..", "fct_string, true!")
                return False
                
            # if # sets comment
            elif not str_char == '"' and not str_char == "'":
                if BIT_DEBUG_PAR: print ("..", "fct_string, false!")
                self.lst_str[3] = False
            
            if str_char == "#":
                if BIT_DEBUG_PAR: print ("..", "bit_comm!")
                self.bit_comm = True
                return False
            
            # starts string
            if str_char == '"' or str_char == "'":
                self.lst_str[0] = True
                self.lst_str[1] = str_char
                if BIT_DEBUG_PAR: print ("..", "fct_string, go!")
                return False
                
        # ends string
        else:
            if BIT_DEBUG_PAR: print ("..","fct_string...")
            if str_char == self.lst_str[1]:
                if BIT_DEBUG_PAR: print ("..", "fct_string, bit_end!")
                self.lst_str[0] = False
                return False
                
        return False
        
    ##########################################################################
    # parsing operator chars
    def fct_sign(self, str_char):
        if self.lst_str[0] or self.bit_comm:
            return False
            
        if re.match(r"\A[+!=&~|<>^*:-]\Z", str_char):
            return True
            
        return False
        
    ##########################################################################
    # parsing name of class, var etc.
    def fct_text(self, str_char):
        if not self.lst_upper[0]: 
            if BIT_DEBUG_PAR: print ("..", "fct_text, lst_upper false")
            self.lst_upper[1] = False
        
        # removes tab finding
        if self.lst_tab[1] > 0:
            if BIT_DEBUG_PAR: print ("..", "fct_text, tab set, close")
            self.int_tree = self.lst_tab[0]
            self.lst_tab[1] = -1
        
        # always text if comment or string
        if self.lst_str[0] or self.bit_comm:
            if str_char == "\\":
                str_char = "+"
            return True
        
        # checks if text
        if re.match(r"\A[\w.*\"']\Z", str_char):
            if self.int_inline == 1:
                if BIT_DEBUG_PAR: print ("..", "fct_text, inline")
                self.int_inline = 2 
                
            return True
            
        return False
        
    ########################################################################## 
    # takes returned char from closed bundle and parse it before new chars
    def fct_reverse(self, str_char):
        if self.str_retrn != "":
            if BIT_DEBUG_PAR: print ("..", "fct_reverse")
            str_char = self.str_retrn
            self.str_retrn = ""
            return str_char
            
        return None
        
    ##########################################################################
    # merge last char from last bundle with current char
    def fct_append(self, str_char):
        if re.match(r"\A[\w]\Z", self.str_retrn):
            str_char = self.str_retrn + str_char
            self.str_retrn = ""
            
        return str_char
        
    ##########################################################################
    # saves current char to history variable
    def fct_sync(self, str_char):
        self.str_hist = str_char
        
    ##########################################################################
    # parsing bracket chars and it's triggered events
    def fct_zagr(self, str_char):
        # bracket open
        if re.match(r"\A[(\[{]\Z", str_char):
            self.int_free += 1 
            self.bit_end = True
            if BIT_DEBUG_PAR: print ("..", "fct_zagr, open")
            return True
        
        # bracket closed
        if re.match(r"\A[)\]}]\Z", str_char):        
            self.int_free -= 1
            self.bit_end = True
            if BIT_DEBUG_PAR: print ("..", "fct_zagr, close")
            return True
            
        return False
        
    ##########################################################################    
    # parsing whitespace and it's triggered events
    def fct_white(self, str_char): 
        if self.bit_comm:
            return False
            
        if self.str_retrn == "\n":
            self.lst_tab[0] = 0
            self.str_retrn = ""
            
        if not self.lst_str[5] and not self.lst_str[3] and str_char == "\\":
            self.bit_newln = True
            self.lst_tab[0] = 0
            if BIT_DEBUG_PAR: print ("..", "fct_white, set \\")
            return True
            
        if ((not self.lst_str[0] and str_char == " ") 
                or (self.bit_newln and str_char == "\n")) \
                or (not self.lst_str[0] and str_char == ","):
            if BIT_DEBUG_PAR: print ("..","fct_white, continue")
            if self.int_free == 0 and self.lst_tab[0] > -2:
                if BIT_DEBUG_PAR: print ("..", "fct_white, tab :", self.lst_tab[0])
                self.lst_tab[0] += 1
                
            if not self.lst_str[0]:
                self.bit_end = True
                
            self.bit_newln = False
            return True
            
        return False
        
    ##########################################################################
    # parsing newline and it's triggered events
    def fct_newset(self, str_char):  
        if not self.lst_str[0] and self.int_free == 0 and not self.bit_newln:
            if not self.bit_comm and str_char == ":":
                if BIT_DEBUG_PAR: print ("..", "fct_newset : lst_tab +", self.str_name)
                if self.lst_tab[1] == 0:
                    self.lst_tab[1] = 1
                self.lst_upper[0] = False
                self.int_inline = 1
                self.bit_end = True
                return True
                
            if str_char == "\n" or not str_char:
                if BIT_DEBUG_PAR: print ("..", "fct_newset \\n lst_tab 0")
                self.lst_tab[0] = 0
                self.bit_comm = False
                if self.int_inline == 1:
                    self.int_inline = 0
                self.bit_end = True
                return True
                
            if not self.bit_comm and str_char == ";":
                if BIT_DEBUG_PAR: print ("..", "fct_newset ;")
                self.lst_tab[0] = 0 # da ne ??
                self.bit_end = True
                return True
                
        elif str_char == "\n" or not str_char and self.int_free > 0:
            self.bit_comm = False
            
        return False
        
    ##########################################################################   
    # saving buffer into bundle
    def fct_save(self, str_buff):
        if isinstance(str_buff, cls_bundle):
            self.str_retrn = str_buff.str_retrn
            self.lst_tab[0] = str_buff.lst_tab[0]
            self.int_inline = 0
            if BIT_DEBUG_PAR: print ("..", "fct_save, return:"
                                + self.str_retrn + ":")
        if self.lst_upper[1]:
            self.lst_head.append(str_buff)
            if BIT_DEBUG_PAR: print ("..", "fct_save, lst_head")
        else:
            self.lst_body.append(str_buff)
            if BIT_DEBUG_PAR: print ("..", "fct_save, lst_body")
        return False
        
    ##########################################################################    
    # preparing end of current char check
    def fct_finish(self, _retrn, bit_fin=False):
        self.str_retrn = _retrn
        self.bit_end = bit_fin
        if not self.lst_upper[0]:
            if BIT_DEBUG_PAR: print ("..", "fct_finish, lst_upper false")
            self.lst_upper[1] = False
            
        if self.bit_fin:
            if BIT_DEBUG_PAR: print ("..", "bit_fin bit_end!")
            return True
            
        self.bit_fin = bit_fin
        if BIT_DEBUG_PAR: print ("..", "bit_fin" )
        return False

        
##############################################################################  
# saves buff to list or opens new bundle instance
def fct_parsave(obj_file, obj_bund, lst_temp, str_buff):
    const = len([itm for itm in LST_PAR_CON if str_buff == itm])
    if BIT_DEBUG_PAR: print ("<<", "..const:%d:" % (const))
    if not obj_bund.bit_comm and obj_bund.int_free == 0 and const > 0:
        if len(lst_temp) > 0:
            if BIT_DEBUG_PAR: print (">>", "..saving, fct_save :", lst_temp)
            obj_bund.fct_save(lst_temp)
            lst_temp = []
            
        bund2 = cls_bundle(str_buff, obj_bund.int_lvl + 1)
        bund2.str_retrn = obj_bund.str_hist
        if BIT_DEBUG_PAR: print ("<<", "..saving obj_bund:"
                            + str_buff + ":", ":" + obj_bund.str_hist + ":")
        obj_bund.fct_save(fct_parser(obj_file, bund2))
        
    elif not re.match(r"\A#|(r?[\"'])", str_buff) and const == 0 : 
        if BIT_DEBUG_PAR: print ("<<", "..saving fct_text:" + str_buff + ":")
        [lst_temp.append(y) 
        for y in re.split(r'([^\w."\' ]{1,2})', str_buff) 
        if y != "" and y != " "
        ] 
        
    else:
        if BIT_DEBUG_PAR: print ("<<", "..saving str_buff:" + str_buff + ":")
        lst_temp.append(str_buff)
        
    return lst_temp
        
##############################################################################        
# main parser (recursive), fills bundle structure
def fct_parser(obj_file, obj_bund):
    lst_temp = []
    str_buff = ""
    str_znak = ""
    str_char = ""
    obj_bund.fct_start()
    
    # go through each character unitil EOF
    while True:
        if BIT_DEBUG_PAR: print ("\n", "##", "while")
        if not obj_bund.bit_end:
            str_char = obj_bund.fct_reverse(str_char)
            if not str_char:
                str_char = obj_file.read(1)
                
            obj_bund.fct_sync(str_char)
            if BIT_DEBUG_PAR: print (">>", "in :" + str_char + ": ret :"
                                + obj_bund.str_retrn + ":")          
            # see if string
            if obj_bund.fct_string(str_char):
                pass
                
            # see if neline
            elif obj_bund.fct_newset(str_char):
                if BIT_DEBUG_PAR: print (">>", "fct_newset %d:%d:%d:" %
                                    (obj_bund.lst_tab[0], 
                                    obj_bund.lst_tab[1], 
                                    obj_bund.int_tree))
                # if neline saves it for return
                if obj_bund.lst_upper[0] or (obj_bund.int_inline > 0 \
                        and not obj_bund.bit_newln and str_char == "\n"):
                    obj_bund.fct_finish(
                        str_char if str_char == "\n" else "", True)
                        
                # appends buffer to list
                if len([itm for itm in LST_PAR_CON 
                        if str_buff == itm]) == 0:
                    if len(str_buff) > 0:
                        lst_temp.append(str_buff)
                        
                    if len(str_znak) > 0:
                        lst_temp.append(str_znak)
                        
                    if BIT_DEBUG_PAR: print (">>", "fct_newset, fct_save :",
                                        lst_temp)
                    obj_bund.fct_save(lst_temp)
                    lst_temp = []   
                    str_buff = ""                
                continue 
                
            # see if whitespace
            elif obj_bund.fct_white(str_char):
                if BIT_DEBUG_PAR: print (">>", "fct_white %d:%d:%d:" %
                                    (obj_bund.lst_tab[0], 
                                    obj_bund.lst_tab[1], 
                                    obj_bund.int_tree))
                                    
            # see if sign and saves buffer 
            elif obj_bund.fct_sign(str_char):
                if BIT_DEBUG_PAR: print (">>", "fct_sign, fct_text + :"
                                    + str_char + ":")
                if len(str_buff) > 0:
                    lst_temp = fct_parsave(obj_file, obj_bund, lst_temp, 
                                            str_buff)
                    str_buff = ""
                str_znak += str_char

            # see if text, saves to list
            elif obj_bund.fct_text(str_char):
                if BIT_DEBUG_PAR: print (">>", "fct_text + :"
                                    + str_char + ": %d:%d:%d:" %
                                    (obj_bund.lst_tab[0], 
                                    obj_bund.lst_tab[1], 
                                    obj_bund.int_tree))
                if BIT_DEBUG_PAR: print (">>",obj_bund.int_free,
                                        ":", obj_bund.int_inline)
                str_char = obj_bund.fct_append(str_char)
                if obj_bund.int_free == 0 and not obj_bund.int_inline \
                        and obj_bund.lst_tab[1] < 1 \
                        and obj_bund.lst_tab[0] < obj_bund.int_tree:
                    if BIT_DEBUG_PAR: print (">>","low lst_tab :"+str_char+":")
                    obj_bund.fct_finish(str_char, True)
                    continue
                    
                if len(str_znak) > 0:
                    lst_temp.append(str_znak)
                    str_znak = ""
                    
                str_buff += str_char
                
            # see if bracket
            elif obj_bund.fct_zagr(str_char):
                pass 
                
        # saves buffer and other stuff before new char
        if obj_bund.bit_end:
            if BIT_DEBUG_PAR: print ("##", "else")
            if len(str_znak) > 0:
                lst_temp.append(str_znak)
                
            # saves bundle
            if len(str_buff) > 0:
                lst_temp = fct_parsave(obj_file, obj_bund, lst_temp, 
                                        str_buff)
                                        
            # saves char
            if re.match(r"\A[()\[\]{},]\Z", str_char): 
                if BIT_DEBUG_PAR: print ("<<", "..saving :,:")
                lst_temp.append(str_char) 
            
            if BIT_DEBUG_PAR: print (">>", "..pre finish %d:%d:%d:" %
                                    (obj_bund.lst_tab[0], 
                                    obj_bund.lst_tab[1], 
                                    obj_bund.int_tree))        
            # sync for char finish
            if obj_bund.fct_finish(obj_bund.str_retrn):
                if BIT_DEBUG_PAR: print ("<<","fct_sync:" + str_char + ":")
                break
                
            str_buff = ""
            str_znak = ""
            
        if not str_char:
            break 
            
        if BIT_DEBUG_PAR: print ("##", "bit_end\n")
        
    if BIT_DEBUG_PAR: print ("##", "return\n")
    return obj_bund
        
##############################################################################
##############################################################################
