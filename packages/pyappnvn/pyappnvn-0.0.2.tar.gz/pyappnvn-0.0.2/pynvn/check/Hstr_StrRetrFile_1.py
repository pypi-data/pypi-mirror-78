from pynvn import dict_str_from_lcsv
from pynvn.excel import (sheet_by_namesheet,
                        activesheet
                        )
from pynvn import filter_lstr
from tkinter import messagebox
from appnvn.RetrFile.hstr import hstr_ex
from pynvn.string import twospace_to_onespace
@hstr_ex
def removespace (
                instr = None, 
                option = "both"
                ):
    """
    remove space from string \n
    instr: input your string \n
    option: stype handling string \n
    """
    rspace_fun = {
                "---> name STYLE from config <---": lambda:  "-------------> Input your function <---------------",
                "---> name STYLE from config <--- ": lambda:  "-------------> Input your function <---------------",
                }
    return rspace_fun[option]()

class rapp:
    """ 
    Generic class for this template with variables\n
    retr_path: directory of execute excel file\n
    retr_sheetname: name of sheet name of retr_path excel\n
    fuction: choose the feature  want to use \n
    pathconf: Directory of path conf (.csv), this path have conf parameter 
    """
    def __init__(self,
                retr_path = None,
                retr_sheetname =None, 
                fuction = "",
                pathconf = None,
                ):
        self.__retr_sheetname = retr_sheetname
        self.__fuction = fuction.lower()
        # Create a dict have parameter from csv 
        self.__dictconf = dict_str_from_lcsv(path=pathconf)
        # Option from user input (Active Sheet or not)
        self.__ws_retr =  activesheet() if retr_sheetname == "Active Sheet"\
                                        else sheet_by_namesheet(path=retr_path,
                                                                namesheet=retr_sheetname
                                                                )
        # Check file excel execute is conf_ex.xlsx or not 
        if self.__ws_retr.name == "hrdata_modified":
            messagebox.showerror("Error Name Excel",
                                "Can not using file excel: conf_ex.xlsx to execute. \
                                Check again {}".format("hrdata_modified")
                                )

    def ft_tool(self):
        """
        execute func of sortware \n
        ex: removespace, capfs

        """
        # filter list string only key from csv
        lfuns = filter_lstr(liststr=list(self.__dictconf.keys()),
                                        reverse_criteria=True,
                                        criteria=["sub_"],
                                        upper = False
                                        )
        # create dict have fun execute 
        mydictfun = {
                    "removespace":(lambda: self.__removespace()),
                    "capfs":(lambda: self.__capfs())
                    }
        # Option from user input function (config or not)
        if self.__fuction == "Config":
            for lfun in lfuns:
                mydictfun[lfun]()
        else:
            mydictfun[self.__fuction]()
    
    def __removespace(self):

        """ 
        For case function "REMOVESPACE" user select from interface 
        """
        cyesornot = self.__dictconf["removespace"]
        rmrange = self.__dictconf["sub_removespace_range"]
        rmstype = self.__dictconf["sub_removespace_style"]
        removespace(ws =self.__ws_retr,
                    rmrange=rmrange, 
                    option=rmstype
                    ) if cyesornot[0] =="yes" else False  
    def __capfs(self):
        """ 
        For case function "CAPFS" user select from interface 
        """
        cyesornot = self.__dictconf["capfs"]
        rmrange = self.__dictconf["sub_capfs_range"]
        rmstype = self.__dictconf["sub_capfs_style"]
        capitalize(rmrange=rmrange,
                        option= rmstype,
                        ws=self.__ws_retr,
                        ) if cyesornot[0] =="yes" else False
