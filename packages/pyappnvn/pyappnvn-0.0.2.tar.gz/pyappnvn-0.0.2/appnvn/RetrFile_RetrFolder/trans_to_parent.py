from tkinter import messagebox
from pynvn.path.ppath import getdirpath,ExtractFileNameFromPath
from pynvn.excel import col2num,colnum_string, repathlinkexcel
import xlwings as xw 
from pynvn.csv.rcsv import returndictrowforcsv
from pynvn.string.slist import returnlist_from_listinstr
from pynvn.string.slist import str_returnliststr
from appnvn.exazp.excel.hchildsheet import hchildsheet
class tparent:
    """copy excel to excel"""
    def __init__(self,
                    pathconf = None,
                    pathdes= None, 
                    pathtocopy= None,
                ):
        # call dict 
        self.dictconf = returndictrowforcsv(path=pathconf)
        # return list sheet excel to handling 
        self.__pathdes = pathdes
        self.__pathtocopy = pathtocopy
        self.__app = xw.App(visible=True,
                            add_book=False
                            )
        self.__desxw = self.__app.books.open(fullname=self.__pathdes,update_links=False)
        self.__copyxw = self.__app.books.open(fullname=self.__pathtocopy,
                                                        update_links=False,                       
                                                        read_only=False,
                                                        ignore_read_only_recommended=False)
        self.wsnames = self.__copyxw.sheets
        for namesheet in self.wsnames:
            if "AZB" in namesheet.name:
                self.ws_copy = namesheet
                break
        
        #max row ws1
        self.rows = self.ws_copy.api.UsedRange.Rows.count
        #max colum ws1
        self.cols = self.ws_copy.api.UsedRange.Columns.count
        self.colunsande = [colnum_string(1),colnum_string(self.cols)]
        # name sheet 
        self.__namesheet = self.ws_copy.name
        # set active sheet name 
        self.__desxw.sheets[self.__namesheet].activate()

    def trans_sheet_to_excel_exist(self):
        """ copy sheet name  to excel existing """
        # get dir path 
        dirpath = getdirpath(self.__pathtocopy)
        # get extract file name from path 
        namefile = ExtractFileNameFromPath(self.__pathtocopy)
        pfile = repathlinkexcel(dpath=dirpath,
                                namefile=namefile,
                                namesheet=self.__namesheet)
        sheet_des = self.__desxw.sheets[self.__namesheet]
        sheet_copy = self.__copyxw.sheets[self.__namesheet]

        recor_l_lint = int(self.dictconf["recor_l1"])
        valueim = returnlist_from_listinstr(self.dictconf["valueim"].replace(":", ","))
        valuehavechild = returnlist_from_listinstr(self.dictconf["valuehavechild"].replace(":", ","))
        msstr =self.dictconf["azb10_ms"]
        forbydup = returnlist_from_listinstr(self.dictconf["zab10_forbydup"].replace(":", ","))
        locuseformulas = returnlist_from_listinstr(self.dictconf["locuseformulas"].replace(":", ","))
        col_dup = returnlist_from_listinstr(self.dictconf["dup"].replace(":", ","))
        # max row sheet des
        self.m_row = sheet_des.range(msstr + str(sheet_des.cells.last_cell.row)).end('up').row
        hchild = hchildsheet(startrow=recor_l_lint,
                        col_key_msa=msstr,
                        pfile=pfile,
                        columnlra=self.colunsande,
                        max_row=self.m_row,
                        lcolumnformulas = locuseformulas,
                        valueim=valueim,
                        sheet_des =sheet_des,
                        sheet_copy=sheet_copy,
                        col_dup=col_dup,
                        max_row_allsheet=self.rows,
                        lvaluehavechild=valuehavechild,
                        formulasfor_col_dup = forbydup)
        self.__copyxw.close()
        self.__desxw.save()
        self.__desxw.close()
        self.__app.quit()