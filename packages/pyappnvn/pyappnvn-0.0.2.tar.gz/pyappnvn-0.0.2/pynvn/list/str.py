from tkinter import messagebox
import ast
import csv
def leftstr (substr = None, symbtoplit = "_"):
    """ left side of sring """
    # len of str
    lenstr = len(substr)
    # returns first occurrence of Substring 
    result = substr.find('_',1,lenstr) 
    # return left
    return left(substr,result)


def splitstrtolist(subtr, symbtoplit = "x"):
    """split str """
    return subtr.split(symbtoplit)

def converliststrtoint(liststr = None, errormsg = "can not convert to int"):
    """ conver list str to int """
    try: 
        res = list(map(int,liststr))
    except:
        messagebox.showerror ("Error",errormsg)
    return res

def left(s, amount):
    """ extract str left """
    return s[:amount]

def exstrtolistint (strp = None, symbtoplitp = "_",symbtoplitsecond = "x" ):
    """ return exstr of list int form string"""
    leftt = leftstr(substr=strp,symbtoplit=symbtoplitp)
    listtr = splitstrtolist(leftt,"x")
    return converliststrtoint (listtr,errormsg="Recheck folder name of child parent folder Folder have to template :widthxheight_infor")

def converlistinstrtolist(path = None):
    """ convert list in string to dict """
    reader = csv.reader(open(path, 'r'))
    return {k:ast.literal_eval(v)  for k,v in reader}

def Concatenatelistofstring(instr = []):
    """ Concatenate a list of strings into one string """
    return ''.join(instr)