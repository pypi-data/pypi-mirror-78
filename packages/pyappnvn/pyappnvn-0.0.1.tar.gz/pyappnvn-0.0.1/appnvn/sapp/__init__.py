from pynvn import dict_str_from_lcsv
from pynvn.excel import (sheet_by_namesheet,
                            activesheet)
from pynvn import filter_lstr
from pynvn.excel.write import hvalues_in_cell
class sapp:
    """ fill the formulas into excel file """
    def __init__(self,
                retr_path = None,
                retr_sheetname =None, 
                fuction = None,
                pathconf = None,
                ):

        self.__dictconf = dict_str_from_lcsv(path=pathconf)
        self.__retr_sheetname = retr_sheetname
        self.__fuction = fuction
        if retr_sheetname == "Active Sheet":
            self.__ws_retr = activesheet()
        else:
            self.__ws_retr = sheet_by_namesheet(path=retr_path,
                                                namesheet=retr_sheetname)

    def ft_tool(self):

        lfuns = filter_lstr(liststr=list(self.__dictconf.keys()),
                                            reverse_criteria=True,
                                            criteria=["sub_"],
                                            upper = False
                                            ) 
        
        mydictfun = {
                    "removespace":(lambda: self.__removespace()),
                    "capfs":(lambda: self.__capfs())
                    }        
        
        if self.__fuction == "Config":
            for lfun in lfuns:
                # remove  space 
                mydictfun[lfun]()
        else:
             mydictfun[self.__fuction]()
    def __removespace(self):
        cyesornot = self.__dictconf["removespace"]
        rmrange = self.__dictconf["sub_removespace_range"]
        rmtyle = self.__dictconf["sub_removespace_style"]
        hvalues_in_cell(rmrange=rmrange,
                        option=rmtyle,
                        ws=self.__ws_retr,
                        option_fun="removespace") if cyesornot[0] =="yes" else False        

    def __capfs(self):
        cyesornot = self.__dictconf["capfs"]
        rmrange = self.__dictconf["sub_capfs_range"]
        hvalues_in_cell(rmrange=rmrange,
                            ws=self.__ws_retr,
                            option_fun="capfs")  if cyesornot[0] =="yes" else False