import re
import ast
from pynvn.list.str import Concatenatelistofstring
def returnseplistintbbystr(strint):
    """ return list int by separate from string
        ex: "BB5:CF100" ---> [5, 100]
     """
    return list(map(int, (re.findall('\d+', strint)))) 

def str_seplistintbbystr(strint):
    """ return list int_str by separate from string
        ex: "BB5:CF100" ---> ['BB5', 'CF100']
    """
    return list(map(str, (re.findall('\w+', strint)))) 
def str_returnliststr (strint):
    """ 
        return list str convert int list 
        ex: '[1,2,3]' ---> [1, 2, 3]
    """
    return ast.literal_eval(strint)
def returnlist_from_listinstr (strint):
    """ 
        return list str convert int list 
        ex: '[1,2,3]' ---> [1, 2, 3]
    """
    return ast.literal_eval(strint)    
def returnliststr_from_str (strint):
    """ 
        return list str from str (only str without int)
        ex: 'AB1001:A2000' ---> [AB,A]
    """
    pattern = '[a-zA-Z]+'
    return re.findall(pattern, strint) 
def str_seplistint_strbystr(strint):
    """ 
    return list int_str by separate from string
    ex: "BB5:CF100" ---> ['BB5', 'CF100']
    """
    return list(map(str, (re.findall('\w+', strint)))) 

def add_sb_to_str(strint = None, specsb = "$"):
    """ return list int_str by separate from string
        ex: "BB5:CF100" ---> $BB$5:$CF$100
    """
    lstr = returnliststr_from_str(strint)
    lint =returnseplistintbbystr(strint)
    return specsb + lstr[0] + specsb + str(lint[0]) + ":" + specsb + lstr[1] + specsb + str(lint[1])  

def __removespace (instr = None, option = "both"):
    """remove space from string"""
    if option == "both":
        return instr.strip()
    if option == "left":
        return instr.lstrip()
    if option == "right":
        return instr.rstrip()
    else:
        messagebox.showerror("Error","No case for this")

def __capitalize(instr = ""):
    return instr.capitalize()


def splitstrtolist(strin = "",pattern = '\s'):
    """"
    split string
    ex: 'The rain in Vietnam.' ----> ['The', 'rain', 'in', 'Vietnam.']
    """
    strin = __removespace(instr=strin,
                            option="both")
    return re.split(pattern, strin) 
def capitalizefs_list (instr = "",pattern='\s'):
    """
    to capital (uppercase) letter.
    
    ex: nguyen van nhuan ---> ['Nguyen', 'Van', 'Nhuan']

    """
    lstr = splitstrtolist(strin=instr,
                            pattern=pattern
                            )
    return list(map(__capitalize,lstr))

def addvaluexk(listf = [],valuetoadd=" "):
    """ add value xen ke """
    liststr = []
    lenc = len(listf)
    for count,ele in enumerate(listf,1):
        if count != lenc:
            liststr.append(ele)
            liststr.append(valuetoadd)
        else:
            liststr.append(ele)
    return liststr


def capitalizefs (instr = "",pattern='\s'):
    """
    to capital (uppercase) letter.
    
    ex: nguyen van nhuan ---> Nguyen Van Nhuan
    """
    lcap = capitalizefs_list(instr = instr,
                            pattern=pattern)
    ladded = addvaluexk(listf=lcap)
    return Concatenatelistofstring(ladded)

def capitalize(instr = "",option = []):
    """capitalize for string """
    upper_all_fun = {
                "fl":lambda: instr.capitalize(),
                "fs": lambda: capitalizefs(instr=instr),
                "upper_all": lambda: instr.upper(),
                "lower_all": lambda: instr.lower(),
                }
    return upper_all_fun[option]()

def capitalizes(instr = "",options = []):
    """capitalizes for string """
    if (instr == "" or instr ==None):
        return instr
    else:
        for option in options:
            instr = capitalize(instr=instr,option=option)
        return instr