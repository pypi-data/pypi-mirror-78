from pynvn.excel.list import pairslistfromexcel,removevalueinlistpair
from pynvn.csv.tocsv import pairlistinlisttocsv
from pynvn.excel import sheet_by_namesheet
import xlwings as xw
class up_conf_ex:

    """

    Update conf from excel to csv \n
    pathconf: Directory to save data conf from csv (.csv) \n
    pathexconf: directory of excel file config to retrieve (.xlsx) \n

    """
    def __init__(self,pathconf,
                    pathexconf):
        self.__pathconf = pathconf
        self.__ws_excel = sheet_by_namesheet(path=pathexconf,
                                            namesheet="hrdata_modified",
                                            visible = True)
    def convertocsv(self):
        """
        convert to csv 
        
        """
        # createv pair list form excel 
        listepairsremoved = removevalueinlistpair(lista=pairslistfromexcel(sheet=self.__ws_excel))
        # to csv
        pairlistinlisttocsv(listvalue=listepairsremoved,
                            pathcsv=self.__pathconf)