from pynvn.check.list import check_list_value
from xlwings.constants import DeleteShiftDirection
from pynvn.excel import colnum_string

def delrowbyrange (incolumndel = 5, 
                        ws = None,
                        startrow =1,
                        endrow = 1000,
                        value_to_end = "VTC",
                        valuetodelete = ["",None],
                        using_value_to_end = True
                        ):
    """ 
    Delete row by value of cell \n
    incolumndel: index of column to delete \n
    ws: worksheet execute \n
    startrow: start row in ws (worksheet) to start  \n
    endrow: row in ws (worksheet) to end  \n
    value_to_end: value to End for loop \n
    valuetodelete: delete row if valule in this \n
    using_value_to_end: option from progamer \n

    """
    for i in range (startrow,endrow):
        valuecompare =ws.range(i,incolumndel ).value 
        if check_list_value(valuetocheck =[valuecompare],
                            not_in_checkvalue= False):
            while True:
                ws.range('{0}:{0}'.format(i)).api.Delete(DeleteShiftDirection.xlShiftUp)
                if check_list_value(valuetocheck=[ws.range(i,incolumndel).value]):
                    break
        if using_value_to_end:
            if ws.range(i,incolumndel).value == value_to_end :
                break
        else:
            lr = ws.range(colnum_string(incolumndel) + str(ws.cells.last_cell.row)).end('up').row
            if lr == i:
                break

def del_row_by_valueinrange (index_col = 5, 
                            ws = None,
                            startrow =1,
                            endrow = 1000,
                            value_to_end = "VTC",
                            valuetodelete = ["",None],
                            using_value_to_end = True
                            ):

    """
    Delete row by value of cell \n
    index_col: index of column to delete \n
    ws: worksheet execute \n
    startrow: start row in ws (worksheet) to start \n
    endrow: row in ws (worksheet) to end  \n
    value_to_end: value to End for loop \n
    valuetodelete: delete row if valule in this \n
    using_value_to_end: option from progamer \n
    """
    for i in range (startrow,endrow):
        valuecompare =ws.range(i,index_col ).value 
        if check_list_value(valuetocheck =[valuecompare],
                            not_in_checkvalue= False):
            while True:
                ws.range('{0}:{0}'.format(i)).api.Delete(DeleteShiftDirection.xlShiftUp)
                if check_list_value(valuetocheck=[ws.range(i,index_col).value]):
                    break
        if using_value_to_end:
            if ws.range(i,index_col).value == value_to_end :
                break
        else:
            lr = ws.range(colnum_string(index_col) + str(ws.cells.last_cell.row)).end('up').row
            if lr == i:
                break