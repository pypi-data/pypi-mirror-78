from pynvn.csv.todict import dict_str_fromlist
from pynvn.excel import sheet_by_namesheet,activesheet,listsheet_by_wb
from pynvn.list.flist import filterlistbylstr
from pynvn.excel.write import hvalues_in_cell,hrangesheet
from pynvn.excel import col2num,ws_by_namesheet,open_wb_by_xl
from pynvn.excel.copy_move_paste import cprange_2wb

class rapp:
    """ fill the formulas into excel file """
    def __init__(self, retr_path = None,
                        retr_sheetname =None, 
                        fuction = None,
                        pathconf = None,
                        path_exell_tem = None
                        ):
        self.__dictconf = dict_str_fromlist(path=pathconf)
        self.__path_exell_tem = path_exell_tem
        self.__retr_sheetname = retr_sheetname
        self.__retr_path = retr_path
        self.__fuction = str(fuction).lower()

    def ft_tool(self):
        lfuns = filterlistbylstr(liststr=list(self.__dictconf.keys()),
                                            criteria_is_not=True,
                                            criteria=["sub_"],
                                            upper = False
                                            ) 
        
        mydictfun = {
                    "copy_from_tem":(lambda: self.__copy_from_tem()),
                    }        
        if self.__fuction == "config":
            for lfun in lfuns:
                mydictfun[lfun]()
        else:
             mydictfun[self.__fuction]()

    def __copy_from_tem(self):
        yerorno = self.__dictconf["copy_from_tem"]
        startcopyrange = self.__dictconf["sub_copy_from_tem_startcopyrange"]
        startpasterange = self.__dictconf["sub_copy_from_tem_startpasterange"]
        namesheet_tem = self.__dictconf["sub_copy_from_tem_namesheet_tem"]
        if self.__retr_sheetname == "Active Sheet":
            ws_retr = activesheet()
            cprange_2wb(pathtocopy=self.__path_exell_tem,
                        range_copy=startcopyrange[0],
                        sheet_des=ws_retr,
                        range_paste=startpasterange[0],
                        clear_rcopy_after_copy=False,
                        sheetname_tem=namesheet_tem[0]
                        ) 
        else:
            wb_retr = open_wb_by_xl(pathex=self.__retr_path,
                                    cre_new_app=False,
                                    visible = True, 
                                    add_book = False
                                    )
            lsheet = listsheet_by_wb(wb_retr)
            for nsheet in lsheet:
                if self.__retr_sheetname in nsheet:
                    wb_retr.sheets[nsheet].activate()
                    ws_retr = activesheet()
                    cprange_2wb(pathtocopy=self.__path_exell_tem,
                                range_copy=startcopyrange[0],
                                sheet_des=ws_retr,
                                range_paste=startpasterange[0],
                                clear_rcopy_after_copy=False,
                                sheetname_tem=namesheet_tem[0]
                                ) 