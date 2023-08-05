from pynvn.excel.list import pairslistfromexcel,removevalueinlistpair
from pynvn.csv.tocsv import pairlistinlisttocsv
from pynvn.excel import sheet_by_namesheet
import xlwings as xw
class hconfazb:
    def __init__(self,pathconf,
                    pathexconf):
        self.pathconf = pathconf
        self.__ws_excel = sheet_by_namesheet(path=pathexconf,
                                            namesheet="hrdata_modified",
                                            visible = True)
    def convertocsv(self):
        """convert to csv """
        # createv pair list form excel 
        listepairsremoved = removevalueinlistpair(lista=pairslistfromexcel(sheet=self.__ws_excel))
        # to csv
        pairlistinlisttocsv(listvalue=listepairsremoved,
                            pathcsv=self.pathconf)