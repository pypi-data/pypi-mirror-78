def filterlistbylstr (criteria = [], 
                        liststr = [],
                        criteriamand = [],
                        criteria_is_not = False,
                        upper = False
                        ):
    """ return list filter by criteria is list str and liststr is str """
    if criteria_is_not:
        if upper:
            return [elestr.upper() for elestr in liststr if (not any(ele in elestr for ele in criteria) and all(elem in elestr for elem in criteriamand))]
        else:
            return [elestr for elestr in liststr if (not any(ele in elestr for ele in criteria) and all(elem in elestr for elem in criteriamand))]
    else:
        return [elestr for elestr in liststr if (any(ele in elestr for ele in criteria) and all(elem in elestr for elem in criteriamand))]

def pairlistandlist(listm, list_str):
    """ return pair of list combine list aphabe """
    return [str(ele[0] + ":" + ele[1]) for ele in  [[list_str[0] +str(eler[0] + 1 ),list_str[1] + str(eler[1] - 1)] for eler in list(zip(listm, listm[1:]))]]


def filterlistbylstr1 (criteria = [], liststr = [],criteriamand = [],reverse_criteria = False):
    return [elestr for elestr in liststr if ele not in elestr for ele in criteria]

def filter_lstr (criteria = [], 
                        liststr = [],
                        criteriamand = [],
                        reverse_criteria = False,
                        upper = False
                        ):
    """ return list filter by criteria is list str and liststr is str """
    if reverse_criteria:
        if upper:
            return [elestr.upper() for elestr in liststr if (not any(ele in elestr for ele in criteria) and all(elem in elestr for elem in criteriamand))]
        else:
            return [elestr for elestr in liststr if (not any(ele in elestr for ele in criteria) and all(elem in elestr for elem in criteriamand))]
    else:
        return [elestr for elestr in liststr if (any(ele in elestr for ele in criteria) and all(elem in elestr for elem in criteriamand))]