from pynvn.excel import col2num,colnum_string, repathlinkexcel
from pynvn.csv.todict import returndictrowforcsv
from pynvn.excel.fomulas import vlookup,sumif,anyfun
from pynvn.excel import (sheet_by_namesheet,
                        activeworkbook_fullname,
                        activesheet_name,
                        activesheet)
import xlwings as xw
from tkinter import messagebox
class fformulas:
    """ fill the formulas into excel file """
    def __init__(self, retr_path = None,
                        retr_sheetname =None, 
                        des_path = None,
                        des_sheetname =None,
                        fuction = None,
                        pathconf = None,
                        ):
        self.dictconf = returndictrowforcsv(path=pathconf)
        self.__retr_sheetname = retr_sheetname
        self.__des_path = des_path
        self.__des_sheetname = des_sheetname
        self.__fuction = fuction

        if retr_sheetname == "Active Sheet":
            retr_path = activeworkbook_fullname()
            retr_sheetname = activesheet_name()

        self.__pexcelretr = repathlinkexcel(usingfullname=True,
                                            fullname=retr_path,
                                            namesheet=retr_sheetname
                                            )
        if des_sheetname == "Active Sheet":
            self.__ws_des = activesheet()
        else:
            self.__ws_des = sheet_by_namesheet(path=des_path,
                                                namesheet=des_sheetname)
    def filltoexcell(self):
        if self.__fuction == "VLOOKUP":
            vlvalue = self.dictconf["sub_vlookup_lookup_value"]
            vTaalue = self.dictconf["sub_vlookup_table_array"]
            vrlalue = self.dictconf["sub_vlookup_range_lookup"]
            clgvalue = self.dictconf["sub_vlookup_column_get_value"]
            clrvvalue = self.dictconf["sub_vlookup_loc"]
            vlookup(loopkup_value_range=vlvalue,
                                table_array=vTaalue,
                                plexcel=self.__pexcelretr,
                                colum_to_get_value = clgvalue,
                                ws_des = self.__ws_des,
                                Sub_VLOOKUP_Locc_result_value= clrvvalue
                                ).forexelldes()
        elif self.__fuction == "SUMIF":
            sirange = self.dictconf["sub_sumif_range"]
            sicriteria = self.dictconf["sub_sumif_criteria"]
            sisum_range = self.dictconf["sub_sumif_sum_range"]
            silrvalue = self.dictconf["sub_sumif_loc"]
            sumif(sirange=sirange,
                    sicriteria=sicriteria,
                    sisum_range=sisum_range,
                    plexcel=self.__pexcelretr,
                    ws_des=self.__ws_des,
                    silrvalue=silrvalue
                    ).forexelldes()
        else:
            any_range = self.dictconf[self.__fuction.lower()]

            any_loc = "sub_" + self.__fuction.lower() + "_loc"
            loc_value = self.dictconf[any_loc]

            anyfun(function_range=any_range,
                    function_loc=loc_value,
                    plexcel=self.__pexcelretr,
                    ws_des=self.__ws_des
                    ).forexelldes()