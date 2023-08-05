from tkinter import messagebox
import xlwings as xw
from pynvn.excel import convertrangaphatonunber,returnrangelastcolumn
def returnactivewbpath (namefile):
    """ return active workbook """
    try:
        fpath = xw.books.active.fullname
        return fpath
    except:
        messagebox.showerror ("Error",
                                        "Not yet open file excel, open excel file {0}".format(namefile))
        