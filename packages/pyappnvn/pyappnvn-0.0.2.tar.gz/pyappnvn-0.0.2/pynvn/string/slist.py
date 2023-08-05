import re
import ast
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

def list_from_listinstr (strint):
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
