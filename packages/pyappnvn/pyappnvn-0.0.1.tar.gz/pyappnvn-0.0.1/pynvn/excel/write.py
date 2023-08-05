from pynvn.string import removespaces
from pynvn.excel import colnum_string
from pynvn.excel.list import lnumbercolumnbyrangstr
from pynvn.string.slist import returnseplistintbbystr
from tkinter import messagebox
from pynvn.string.list import capitalizes
from pynvn.excel.del_row import delrowbyrange
from pynvn.excel.rows import startrow_endrow

class hrangesheet:
    """ 
    handling range for sheet\n
    rmrange: Range to handling string: \n
    ex: A1, A1:B3,A
    ws: worksheet corresponds to the rmrange \n
    option: style to  handling:\n
    ex: tspacetoospace, fs,upper_all,both, left, right,lower_all,all \n
    option_fun: For case function "REMOVESPACE or CAPFS" user select from interface \n
    ex: REMOVESPACE,CAPFS

    """
    def __init__(self,
                rmrange = [], 
                option = [],
                ws = None,
                option_fun = "removespace",
                feature_fun = "hstr",
                **kw
                ):
        self.__option = option
        self.__ws = ws
        self.__option_fun = option_fun
        self.__feature_fun = feature_fun
        for rangea in rmrange:
            self.__cols=lnumbercolumnbyrangstr(rstr=rangea)
            self.__rows=returnseplistintbbystr(strint=rangea)
            self.__vcell(**kw)

    def __vcell(self,**kw):
        """ 
        remove space in excel by ws col and row 
        """
        a,b = startrow_endrow(ws=self.__ws,
                                rows=self.__rows,
                                cols=self.__cols
                                )
        for col in self.__cols:
            if self.__feature_fun == "hstr":
                hstr_in_range(st_row=a,
                                end_row = b,
                                index_col=col,
                                option=self.__option,
                                ws=self.__ws,
                                option_fun = self.__option_fun
                            )
            else:
                delrowbyrange(incolumndel=col,
                                ws=self.__ws,
                                startrow=a,
                                endrow=b,**kw)
        
def hstr_in_range(st_row, 
                    end_row,
                    index_col,
                    option = [],
                    ws = None,
                    option_fun = None
                ):
    """
    handling string in range \n
    st_row: start row  sheet \n
    end_row: end row  sheet \n
    ws: worksheet input \n
    option: style to  handling:\n
    ex: tspacetoospace, fs,upper_all,both, left, right,lower_all,all \n  
    option_fun: For case function "REMOVESPACE or CAPFS" user select from interface \n
    """
    for i in range(st_row,end_row + 1): 
        valuee = ws.range(i,index_col).value
        myDictfun = {
                    "removespace": (lambda : removespaces(instr=valuee,
                                                        options=option
                                                        )
                                    ),
                    "capfs": (lambda : capitalizes(instr=valuee,
                                                    options=option
                                                    )
                            ),                              
                    }
        nvalue = myDictfun[option_fun]()
        ws.range(i,index_col).value = nvalue
