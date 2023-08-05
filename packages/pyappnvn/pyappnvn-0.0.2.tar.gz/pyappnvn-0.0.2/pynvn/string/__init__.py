from tkinter import messagebox
import re
import csv
import ast
def sepnumberandstrfromstr (sstr):
    """Splitting text and number in string"""
    # Splitting text and number in string 
    try:
        temp = re.compile("([a-zA-Z]+)([0-9]+)(\D)([a-zA-Z]+)([0-9]+)") 
        return temp.match(sstr).groups() 
    except:
        messagebox.showerror ("error input","Check your input {}, it must aann:aann".format(sstr))
def returnrangewolastrow(sstr):
    """Splitting text and number in string"""
    try:
        temp = re.compile("([a-zA-Z]+)([0-9]+)(\D)([a-zA-Z]+)") 
        return temp.match(sstr).group() 
    except:
        messagebox.showerror ("error input","Check your input {}, it must aann:aann".format(sstr))
def restrnotspaceifhavespace(instr = None,revalue = "None"):
    """ remove space from string"""
    return instr.replace(" ", "")

def no_accent_vietnamese(s):
    """Remove Vietnamese Accents"""
    if isinstance(s,str):
        s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
        s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
        s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
        s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
        s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
        s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
        s = re.sub(r'[ìíịỉĩ]', 'i', s)
        s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
        s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
        s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
        s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
        s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
        s = re.sub(r'[Đ]', 'D', s)
        s = re.sub(r'[đ]', 'd', s)
    return s
def converlistinstrtolist(listinstr = '["A","B" ,"C" ," D"]', path = None):
    """ convert list in string to list """
    reader = csv.reader(open(path, 'r'))
    return {k:ast.literal_eval(v)  for k,v in reader}
def removespace (instr = None, 
                option = "both"
                ):
    """remove space from string"""
    rspace_fun = {
                  "both": lambda: instr.strip(),
                  "left": lambda: instr.lstrip(),
                  "right": lambda: instr.rstrip(),
                  "tspacetoospace": lambda: twospace_to_onespace(instr=instr),
                  "all": lambda: instr.replace(" ", "")
                }
    return rspace_fun[option]()

def removespaces(instr = "", 
                options = []):

    """
    Remove space from string with list option \n
    instr: input string to function \n
    options: features for user input
    
    """
    if (instr == "" or instr ==None):
        return instr
    else:
        for option in options:
            instr = removespace(instr=instr,
                            option=option)
        return instr
        
def allspaces_to_onespace(instr = None):
    """
    remove multiple spaces in a string to one space 
    ex: "The     quick brown    fox" to 'The quick brown fox'
    """
    return re.sub(' +', ' ', instr)


def allspaces_to_onespace(instr = None):
    """
    remove multiple spaces in a string to one space 
    ex: "The     quick brown    fox" to 'The quick brown fox'
    """
    return re.sub(' +', ' ', instr)


def cformat_str(instr = None):
    """ check format of str """
    instr =  instr.replace(" ", "")
    if re.match("^([a-zA-Z]+)$",instr):
        return "a"
    if re.match("^([0-9]+)$",instr):
        return "n"
    if re.match("(^[a-zA-Z]+)([0-9]+)$",instr):
        return "an"
    if re.match("([a-zA-Z]+)([0-9]+)(\D)([a-zA-Z]+)([0-9]+)$",instr):
        return "anan"
    else:
        messagebox.showerror ("Error", "check format {0}".format(instr))
def remove_all_space (instr = None):
    """ remove all space """
    instr.replace(" ", "")
