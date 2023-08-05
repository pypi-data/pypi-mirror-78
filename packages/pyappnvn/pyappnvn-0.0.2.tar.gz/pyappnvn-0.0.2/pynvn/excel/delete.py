
def delrowbyindexcell (incolumndel = "C", 
                        valueofindexcoldel = None, 
                        wb = None,
                        namesheet = None,
                        startrow =1,
                        endrow = 1000,
                        valuetoendrow = "VTC"
                        ):
    """ delete row by value of cell """
    for i in range (startrow,
                        endrow):
        valuecompare =wb.sheets[namesheet].range(i,
                                                incolumndel ).value 
        k = i
        if (valuecompare == None or valuecompare == ""):
            while True:
                wb.sheets[namesheet].range('{0}:{0}'.format(k)).api.Delete(DeleteShiftDirection.xlShiftUp)
                if (wb.sheets[namesheet].range(k,incolumndel).value != None and (wb.sheets[namesheet].range(k,incolumndel).value != "")) :
                    break
        if wb.sheets[namesheet].range(k,incolumndel).value == valuetoendrow :
            break
def delrowbyrange (incolumndel = "C", 
                        valueofindexcoldel = None, 
                        ws = None,
                        startrow =1,
                        endrow = 1000,
                        value_to_end = "VTC",
                        valuetodelete = ["",None]
                        ):
    """ delete row by value of cell """
    
    for i in range (startrow,endrow):
        valuecompare =ws.range(i,incolumndel ).value 
        k = i
        if (valuecompare == None or valuecompare == ""):
            while True:
                ws.range('{0}:{0}'.format(k)).api.Delete(DeleteShiftDirection.xlShiftUp)
                if (ws.range(k,incolumndel).value != None and (ws.range(k,incolumndel).value != "")) :
                    break
        if ws.range(k,incolumndel).value == value_to_end :
            break