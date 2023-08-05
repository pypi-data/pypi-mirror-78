from pynvn.list import listpairfrom2list,convertoint_ifisfloat
from pynvn.string.slist import returnliststr_from_str
import string
def listbyrangeremoveduplicate(sheetexcel,rangea):
    """ return list excel remove duplicate"""
    return list(set(sheetexcel.range(rangea).value))

def listbyrange(sheetexcel,rangea,removeduplicate = False):
    """ return list excel by range"""
    if removeduplicate:
        return list(set(sheetexcel.range(rangea).value))
    else:
        return sheetexcel.range(rangea).value

def pairslistfromexcel (startrow= 1, 
                        floc = "A", 
                        sloc = "B",
                        convetfloattointat_slot = True,
                        sheet = None,
                        ):
    """ create pair list from floc and sloc of excel """
    # max row at floc 
    m_rowatfloc = sheet.range(floc + str(sheet.cells.last_cell.row)).end('up').row
    # create list from range at floc 
    listfloc = sheet.range("{0}{1}:{0}{2}".format(floc,startrow,m_rowatfloc)).value
    # create list from range at sloc 
    listsloc = sheet.range("{0}{1}:{0}{2}".format(sloc,startrow,m_rowatfloc)).value
    if convetfloattointat_slot:
        listsloc = convertoint_ifisfloat(listsloc)
        
    return listpairfrom2list(list_a=listfloc,
                            list_b=listsloc)

def remove2side_pair(lpair):
    """ 
        remove 2 side space list pair ele
        ex: ["  abc",1] ---> ["abc",1]
    """

    return [remove2side(lpair[0]),remove2side(lpair[1])]

def remove2side(in_para):
    """ 
    remove 2 side keep int, remove str 
    ex: "  kkk"----> "kkk"
            12 ---> 12
    """

    if (type(in_para) == int or type(in_para) == float):
        return in_para
    else:
        return str(in_para).strip()
    
def remove_2side_space_byindex_plist(l_instr = [],side = "both"):
    """ remove 2 side space by index pair list """
    if side == "both":
        return list(map(remove2side_pair, l_instr))

def removevalueinlistpair(lista,
                        deleteifvalue = [None,""],
                        lower_index_0 = True,
                        remove_2side_space_index_0_1 = True
                        ):
    """
    remove value in list pair by list deleteifvalue
    """
    if lower_index_0:
        listpair = [[pairarr[0].lower(),pairarr[1]] for pairarr in lista if pairarr[0] not in deleteifvalue]
    if remove_2side_space_index_0_1:
        listpair = remove_2side_space_byindex_plist(l_instr=listpair)
    else:
        listpair = [pairarr for pairarr in lista if pairarr[0] not in deleteifvalue]
    return listpair

def lnumbercolumnbyrangstr (rstr = None):
    """ return range number by rstr by excel column """
    lstr = returnliststr_from_str(strint=rstr)
    if len(lstr) == 2:
        a,b = lstr
        return [inte for inte in range(_col2num(a),_col2num(b) +1)]
    elif len(lstr) == 1:
        return [_col2num(lstr[0])]

def lacolumnbyrangstr (rstr = []):
    """ return range string by rstr by excel column """
    lint = lnumbercolumnbyrangstr(rstr=rstr)
    return list(map(_colnum_string,lint))

def _col2num(col):
    """Return number corresponding to excel-style column."""
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num

def _colnum_string(n):
    """conver colum number become string"""
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def modify_listpair(lista,
                    deleteifvalue = [None,""],
                    lower_index_0 = True,
                    remove_all_space_index_1 = True
                    ):
    """
    remove value in list pair by list deleteifvalue
    """

    if (lower_index_0 == True and remove_all_space_index_1 == True):

        listpair = [[pairarr[0].lower(),pairarr[1].replace(" ", "")] for pairarr in lista if pairarr[0] not in deleteifvalue]

    elif (lower_index_0 == True and remove_all_space_index_1 == False) :

        listpair = [[pairarr[0].lower(),pairarr[1]] for pairarr in lista if pairarr[0] not in deleteifvalue]

    else:

        listpair = [pairarr for pairarr in lista if pairarr[0] not in deleteifvalue]

    return listpair