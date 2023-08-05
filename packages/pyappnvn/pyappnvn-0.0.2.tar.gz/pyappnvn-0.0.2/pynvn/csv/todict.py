import ast
import csv
import re
def strincsvtodict(path = None):
    """ convert list in string to dict """
    reader = csv.reader(open(path, 'r'))
    return {k:ast.literal_eval(v)  for k,v in reader}

def returndictrowforcsv (path):
    """ count number of row in csv """
    with open(path, 'r') as readFile:
        listk = {lcsv[0]:lcsv[1] for lcsv in list(csv.reader(readFile, delimiter=','))}
    return listk


def dict_str_fromlist(path = None):
    """ 
    convert list in string to dict 
    ex: csv content: "r,A1,A2,A3" ---> dict: {r: ["A1","A2","A3"}
    
    """
    reader = csv.reader(open(path, 'r'))
    return {k:re.split("[,]", v)  for k,v in reader}


def dict_from_csv2col (path):
    """ retriver dict from two column in csv """
    with open(path, 'r') as readFile:
        listk = {lcsv[0]:lcsv[1] for lcsv in list(csv.reader(readFile, delimiter=','))}
    return listk

def evallist(n):
    try:
        return eval(n)
    except:
        return n

def dictfromcsv2col_evallist(path):
    """ retrieve dict from two column in csv """
    with open(path, 'r') as readFile:
        listk = {lcsv[0]:evallist(lcsv[1]) for lcsv in list(csv.reader(readFile, delimiter=','))}
    return listk

def dictFcsv_2col_eval_list(path):
    """ retrieve dict from two column in csv """
    with open(path, 'r') as readFile:
        listk = {lcsv[0]:evallist(lcsv[1]) for lcsv in list(csv.reader(readFile, delimiter=','))}
    return listk

def dict_str_from_lcsv(path = None):
    """ 
    convert list in string to dict 
    ex: csv content: "r,A1,A2,A3" ---> dict: {r: ["A1","A2","A3"}
    
    """
    reader = csv.reader(open(path, 'r'))
    return {k:re.split("[,]", v)  for k,v in reader}