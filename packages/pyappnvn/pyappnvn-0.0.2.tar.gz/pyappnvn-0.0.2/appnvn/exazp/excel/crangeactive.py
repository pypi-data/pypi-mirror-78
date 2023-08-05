from pynvn.excel.copypasteexell import cprange
import xlwings as xw
from pynvn.csv.rcsv import returndictrowforcsv
from pynvn.string.slist import returnseplistintbbystr
from pynvn.excel import activesheet,activeworkbook
from pynvn.csv.tolist import convertcsvto1list
from pynvn.path.ppath import (refullpath,
                                getdirpath
                                )
class crangeactive:
    """ copy sheet and change value cell """
    def __init__(self,
                pathconf = None,
                pathconfigexcelcopy = None):
        # call dict 
        self.pathconfigexcelcopy = pathconfigexcelcopy
        dictconf = returndictrowforcsv(path=pathconf)
        self.__hm_startcopyrange = dictconf["hm_startcopyrange"]
        self.fname = dictconf["khns_namfile"] 
        self.__startcopyrange = returnseplistintbbystr(self.__hm_startcopyrange)
        self.__hm_startpasterange = dictconf["hm_startpasterange"]
        self.__hm_hangmuc = dictconf["hm_hangmuc"]
        # copy another range botton
        self.__hm_startcopyrangebt = dictconf["hm_startcopyrange_bt"]
        self.__startcopyrangebt = returnseplistintbbystr(self.__hm_startcopyrangebt)
        self.__hm_startpasterangebt = dictconf["hm_startpasterange_bt"]
        self.pathlsn = refullpath(dirpath=getdirpath(pathconf),
                                        filename=dictconf["listsheetnamehm"])
        self.copyhm = dictconf["copyhm"]

    def copyrangfromconf(self): 
        # return csv have list sheet name 
        try:                        
            self.lsheetname = convertcsvto1list(path=self.pathlsn)
        except:
            pass
        if self.copyhm.strip() == "all":
            self.wb = activeworkbook(namefile=self.fname,
                                    checknamefile= True)
            for sheet in self.lsheetname:
                self.wb.sheets[sheet].activate()
                self.__sheetdesactive = activesheet()
                self.__copyrangfromconfk()
        else:
            self.__sheetdesactive = activesheet()
            self.__copyrangfromconfk()

    def copyrangfromconf_bt(self,acsheet = None):
        cprange(pathtocopy=self.pathconfigexcelcopy,
                pathtodes=acsheet,
                rangetocopy=self.__hm_startcopyrangebt,
                rangetopaste=self.__hm_startpasterangebt
                )
    def __copyrangfromconfk(self):
        start,end = self.__startcopyrange
        cprange(pathtocopy=self.pathconfigexcelcopy,
                pathtodes=self.__sheetdesactive,
                rangetocopy=self.__hm_startcopyrange,
                rangetopaste=self.__hm_startpasterange
                )
        self.__sheetdesactive.range("{0}{1}:{0}{2}".format(self.__hm_hangmuc,
                                                            start + 2,end)).value  =\
                                                                self.__sheetdesactive.name
