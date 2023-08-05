import xlwings as xw 
from tkinter import messagebox
from pynvn import dict_from_csv2col
from pynvn.list.flist import filterlistbylstr
from pynvn.excel.copy_move_paste import co_paste_move_range
from pynvn.excel import activesheet,open_wb_byxl,listsheet_by_wb
from pynvn import dict_from_csv2col
from appnvn.rearrapp.mrange import hsheet_range,hsheet_range_2wb

class rearr_range:
    def __init__(self,lpath_excel =[],
                pathconf = None,
                fuction = None,
                path_exell_tem = None
                ):
        self.__path_exell_tem = path_exell_tem
        self.__lpath_excel = lpath_excel
        self.__fuction = fuction.lower()
        self.__pathconf = pathconf
        self.__dictconf = dict_from_csv2col(pathconf)
        self.lfuns = filterlistbylstr(liststr=list(self.__dictconf.keys()),
                                            criteria_is_not=True,
                                            criteria=["sub_"],
                                            upper = False
                                            )

    def mrange(self):
        mydictfun = {"move_range":(lambda: self.__move_range()),
                    "mrange_by_cell":(lambda: self.__mrange_by_cell()),
                    "copy_from_tem":(lambda: self.__copy_from_tem())
                    }
        for lexel in self.__lpath_excel:
            self.wb = open_wb_byxl(lexel)
            if self.__fuction == "config":
                    for lfun in self.lfuns:
                        mydictfun[lfun]()
            else:
                mydictfun[self.__fuction]()
            self.wb.save()
            self.wb.app.quit()       

    def __move_range(self):
        mrange = self.__dictconf["move_range"]
        sheet_name = self.__dictconf["sub_move_range_sheetname"]
        range_copy = self.__dictconf["sub_move_range_range_copy"]
        range_des = self.__dictconf["sub_move_range_range_des"]
        hsheet_range(sheet_name=sheet_name,
                    wb=self.wb,
                    range_copy=range_copy,
                    range_paste=range_des,
                    clear_rcopy_after_copy=True
                    ) if mrange == "yes" else False                   
    def __mrange_by_cell(self):
        mrange = self.__dictconf["mrange_by_cell"]
        sheet_name= self.__dictconf["sub_mrange_by_cell_sheetname"]
        range_copy = self.__dictconf["sub_mrange_by_cell_loc_range_copy"]
        range_des = self.__dictconf["sub_mrange_by_cell_loc_range_des"]
        hsheet_range(sheet_name=sheet_name,
                    wb=self.wb,
                    range_copy=range_copy,
                    range_paste=range_des,
                    clear_rcopy_after_copy=True,
                    usinglocinexcel=True
                    ) if mrange == "yes" else False
    
    def __copy_from_tem(self):
        mrange = self.__dictconf["copy_from_tem"]
        sheet_name= self.__dictconf["sub_move_range_sheetname"]
        startcopyrange = self.__dictconf["sub_copyfromtem_startcopyrange"]
        startpasterange = self.__dictconf["sub_copyfromtem_startpasterange"]
        namesheet_tem = self.__dictconf["sub_copy_from_tem_namesheet_tem"]
        self.wb_tem = open_wb_byxl(self.__path_exell_tem)
        hsheet_range_2wb(sheet_name=sheet_name,
                    range_copy=range_copy,
                    range_paste=range_des,
                    clear_rcopy_after_copy=False,
                    wb_des=self.wb,
                    wb_tem=self.wb_tem,
                    usinglocinexcel=False,
                    namesheet_tem=namesheet_tem
                    ) if mrange == "yes" else False