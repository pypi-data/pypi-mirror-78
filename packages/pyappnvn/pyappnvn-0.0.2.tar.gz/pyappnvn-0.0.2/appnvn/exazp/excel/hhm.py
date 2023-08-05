from pynvn.csv.rcsv import returndictrowforcsv
from pynvn.excel.list import listbyrange
from pynvn.excel import returnrangelastcolumn
from pynvn.string.slist import returnseplistintbbystr
from pynvn.string.slist import returnlist_from_listinstr
import xlwings as xw
from pynvn.excel import activesheet,activeworkbook
from pynvn.path.ppath import refullpath,getdirpath
from pynvn.csv.tolist import convertcsvto1list
class hdatahm:
    """h data in hang muc """
    def __init__ (self, pathconf = None):
        self.__pathconf = pathconf
        dictconf = returndictrowforcsv(path=pathconf)
        self.__hm_congtac = dictconf["hm_congtac"]
        self.__hm_bombt = dictconf["hm_bombt"]
        self.__hm_macmtc = dictconf["hm_macmtc"]
        self.__hm_materiasvattu = dictconf["hm_materiasvattu"]
        self.__hm_vlvk = dictconf["hm_vlvk"]
        self.__hm_VLTP = dictconf["hm_vltp"]
        self.__hm_MNCTP = dictconf["hm_mnctp"] 

        self.__hm_VTKCT = dictconf["hm_vtkct"]
        self.__hm_NCKCT = dictconf["hm_nckct"] 

        self.__hm_startpasterange = dictconf["hm_startpasterange"]
        sign_vk = dictconf["sign_vk"].replace(":", ",")
        self.sign_vk = returnlist_from_listinstr(sign_vk)
        sign_BT = dictconf["sign_bt"].replace(":", ",")
        self.sign_BT = returnlist_from_listinstr(sign_BT)
        self.__startpasterange = returnseplistintbbystr(self.__hm_startpasterange)

        self.pathlsn = refullpath(dirpath=getdirpath(pathconf),
                                        filename=dictconf["listsheetnamehm"])
        fct = dictconf["fct"]
        try:                        
            self.lsheetname = convertcsvto1list(path=self.pathlsn)
        except:
            pass
        fname = dictconf["khns_namfile"] 
        if fct.strip() == "all":
            self.wb = activeworkbook(namefile=fname,
                                    checknamefile= True)
            for sheet in self.lsheetname:
                print (sheet)
                self.wb.sheets[sheet].activate()
                self.__sheetdesactive = activesheet()
                self.m_row = self.__sheetdesactive.range(self.__hm_congtac + str(self.__sheetdesactive.cells.last_cell.row)).end('up').row
                self.__hdata()
                #self.copyrangfromconf()
        else:
            self.__sheetdesactive = activesheet()
            #self.copyrangfromconf()
            self.m_row = self.__sheetdesactive.range(self.__hm_congtac + str(self.__sheetdesactive.cells.last_cell.row)).end('up').row
            self.__hdata()   
    def __hdata (self):
        for ct in range (self.__startpasterange[0] + 2,self.m_row + 2):
            ctname = self.__sheetdesactive.range("{0}{1}".format(self.__hm_congtac,ct)).value
            if ctname == None or ctname == "":
                continue
            if type(ctname) != str:
                if "62"in str(ctname):
                    self.__sheetdesactive.range("{0}{1}".format(self.__hm_VTKCT,ct)).value = "={0}{1}".format(self.__hm_materiasvattu,ct)
                
                    self.__sheetdesactive.range("{0}{1}".format(self.__hm_NCKCT,ct)).value = "=BG{0}+BH{0}".format(ct)
                else:
                    self.__sheetdesactive.range("{0}{1}".format(self.__hm_VLTP,ct)).value = "={0}{1}".format(self.__hm_materiasvattu,ct)
                
                    self.__sheetdesactive.range("{0}{1}".format(self.__hm_MNCTP,ct)).value = "=BG{0}+BH{0}".format(ct)

            else:
                if any(elen in ctname for elen in self.sign_BT):
                    self.__sheetdesactive.range("{0}{1}".format(self.__hm_bombt,ct)).value = "={0}{1}".format(self.__hm_macmtc,ct)
                if any(elen in ctname for elen in self.sign_vk):
                    self.__sheetdesactive.range("{0}{1}".format(self.__hm_vlvk,ct)).value = "={0}{1}".format(self.__hm_materiasvattu,ct)