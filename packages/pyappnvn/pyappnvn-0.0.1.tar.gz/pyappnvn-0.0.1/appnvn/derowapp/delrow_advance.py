from pynvn.csv.todict import dict_str_fromlist
from pynvn.excel import (sheet_by_namesheet,
                        activesheet)
import xlwings as xw
from tkinter import messagebox
from pynvn.list.flist import filterlistbylstr
from pynvn.excel.write import hrangesheet
from pynvn.excel.hrow import hrow
from pynvn.excel.del_row import del_row_by_valueinrange

@hrow
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

class rapp:
    """
    using for template gui app \n
    retr_path: directory excel file retrieve \n
    retr_sheetname: sheet name of excel file execute \n
    pathconf: using to save config data from excel config
    """
    def __init__(self, retr_path = None,
                        retr_sheetname =None, 
                        fuction = None,
                        pathconf = None,
                        ):
        self.dictconf = dict_str_fromlist(path=pathconf)
        self.__retr_sheetname = retr_sheetname
        self.__fuction = str(fuction).lower()

        if retr_sheetname == "Active Sheet":
            self.__ws_retr = activesheet()
        else:
            self.__ws_retr = sheet_by_namesheet(path=retr_path,
                                                namesheet=retr_sheetname)
    def ft_tool(self):
        lfuns = filterlistbylstr(liststr=list(self.dictconf.keys()),
                                            criteria_is_not=True,
                                            criteria=["sub_"],
                                            upper = False
                                            ) 
        mydictfun = {
                    "delete_row":(lambda: self.__delete_row()),
                    }        
        if self.__fuction == "config":

            for lfun in lfuns:

                mydictfun[lfun]()
        
        else:
             mydictfun[self.__fuction]()

    def __delete_row(self):
        cyesornot = self.dictconf["delete_row"]
        rmrange = self.dictconf["sub_delete_row_range"]
        valuetodel = self.dictconf["sub_delete_row_valuetodelete"]
        valuetodel = list(map(Eval_none_in_list,valuetodel))

        del_row_by_valueinrange(rmrange=rmrange,
                                ws=self.__ws_retr,
                                value_to_end=None,
                                valuetodelete=valuetodel,
                                using_value_to_end=False
                                ) if cyesornot[0] =="yes" else False
        """
        hrangesheet(rmrange=rmrange,
                    ws=self.__ws_retr,
                    value_to_end=None,
                    valuetodelete=valuetodel,
                    using_value_to_end=False
                    ) if cyesornot[0] =="yes" else False
        """
         
def Eval_none_in_list(n):
    """ Eval str "None" None """
    return eval(n) if n=="None" else n
