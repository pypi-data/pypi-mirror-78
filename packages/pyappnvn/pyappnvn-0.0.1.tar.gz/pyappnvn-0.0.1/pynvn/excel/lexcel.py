
from tkinter import messagebox
import openpyxl as xl 
class listexcel:
    """ return list excel or list sheet """
    def __init__ (self, 
                    l_ex = None, 
                    index = 0):

        self.l_ex = l_ex
        self.index = index
    def returnlsheet(self):
        """ return list sheet name  follow list sheet """
        wsl = []
        for els in self.l_ex:
            try:
                elop = xl.load_workbook(els)
                sname = elop.sheetnames[0]
                wsl.append(sname)
            except:
                messagebox.showerror("Error","check file name excel: {0} close it if it is opening".format(els))
        return wsl
