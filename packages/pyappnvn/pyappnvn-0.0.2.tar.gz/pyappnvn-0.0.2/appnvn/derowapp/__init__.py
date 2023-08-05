from pynvn.csv.todict import dict_str_fromlist
from pynvn.excel import (sheet_by_namesheet,
                        activesheet)
import xlwings as xw
from tkinter import messagebox
from pynvn.list.flist import filterlistbylstr
from pynvn.excel.write import hrangesheet

class rapp:
    """ fill the formulas into excel file """
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
        valuetodel = list(map(noneinlist_str,valuetodel))
        hrangesheet(rmrange=rmrange,
                    ws=self.__ws_retr,
                    option_fun="delete_row",
                    feature_fun="delete_row",
                    value_to_end=None,
                    valuetodelete=valuetodel,
                    using_value_to_end=False
                    ) if cyesornot[0] =="yes" else False
         

def noneinlist_str(n):
    """ Evel str "None" None """
    return eval(n) if n=="None" else n
