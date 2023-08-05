import openpyxl as xl
import xlwings as xw
from tkinter import messagebox,Label
from pynvn.excel.hdata import hexcel_sep
from pynvn.path.ppath import getdirpath,refullpath
from pynvn.csv.rcsv import returndictrowforcsv
from pynvn.excel import col2num,book_by_path

class hexcel_child:
    """copy excel to excel"""
    def __init__(self,
                    pathtocopy= None,
                    namesheetchild = "AZB",
                    pathconf = None,
                    diplaywindow  = None
                ):
        self.diplaywindow = diplaywindow
        self.pathconf = pathconf
        self.pathtocopy = pathtocopy
        self.namesheetchild = namesheetchild
        self.dicrowconf = returndictrowforcsv(path=pathconf)
        self.__namefile=self.dicrowconf["khns_namfile"]
        self.__Getlistsheet()
    def __Getlistsheet(self):
        self.__app = xw.App(visible=True,
                            add_book= False)
        self.__wb1  = self.__app.books.open(self.pathtocopy,
                                            update_links=False)
        #self.__wb1  = xw.Book(self.pathtocopy)
        #self.__wb1  = book_by_path(path=self.pathtocopy, visible = False)
        self.names = self.__wb1.sheets
        self.lsheetname = [sheet.name for sheet in self.names]
        self.__ws1 = self.__wb1.sheets[self.names[0]] 
        self.__wsname = self.__ws1.name
        # set active sheet
        
        #max row ws1
        self.rows = self.__ws1.api.UsedRange.Rows.count
        #max colum ws1
        self.cols = self.__ws1.api.UsedRange.Columns.count
        # check name sheet (have to have AZB)
        if self.namesheetchild  in self.__wsname:
            pass
        else:
            messagebox.showerror("error", 
                                "Name sheet must start \
                                from symbols {}...".format(self.namesheetchild))

        self.__dirpath = getdirpath(self.pathtocopy)

        self.__fpath = refullpath(dirpath=self.__dirpath,
                                        filename=self.__namefile)

        #self.__wbthns  = book_by_path(path=self.__fpath, visible = False)
        #self.__wbthns  = xw.Book(self.__fpath)
        self.__wbthns  = self.__app.books.open(self.__fpath,
                                            read_only=True,
                                            ignore_read_only_recommended=True,
                                            update_links=False
                                            )

        self.__wb1.sheets[self.__wsname].activate()

        if self.__wbthns == None:
            messagebox.showerror ("Error directory", "Directory {0} not exists, \
                                recheck Directory again Note: extension of excel maybe xls or xlsx,\
                                     check file config {1} have parameter 'khns_namfile'".format(self.__fpath,self.pathconf))
        
    def runaz30azb60(self, onlyitemiden = False):
        """ run AZB30 and run AZB60"""
        exelh = hexcel_sep(wsheet=self.__ws1,
                                dpath=self.__dirpath,
                                namefile=self.__namefile,
                                dicrowconf = self.dicrowconf,
                                wbnsct=self.__wbthns,
                                pathconf = self.pathconf
                                )
        print (self.lsheetname[0])
        if self.lsheetname[0] == "AZB-30":
            if onlyitemiden:
                exelh.itemiden()
            exelh.habz30()
        if self.lsheetname[0] == "AZB-60":
            exelh.habz60()
        if self.lsheetname[0] == "AZB-50" :
            exelh.azb50()
        if self.lsheetname[0] == "AZB-40" :
            exelh.azb40()
        try:
            self.__wb1.save()
        except:
            messagebox.showerror("error",
                                    "Check path for Pfile {}".format(self.pathtocopy))
        
        #self.__wbthns.app.quit()
        self.__wbthns.close()
        self.__wb1.close()
        self.__app.quit()