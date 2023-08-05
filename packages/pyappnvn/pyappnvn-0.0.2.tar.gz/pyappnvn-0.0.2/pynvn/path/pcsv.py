import csv
from pynvn.data import returnvaluelist
class csvdata:
    def __init__(self,path_Cof = None,
                     NumberRow = 0
                                    ):
        self.path_Cof = path_Cof
        self.NumberRow = NumberRow

    def ReturnDataAllRowByIndexpath (self):
        #open and read excel 
        with open(self.path_Cof) as csvFile:
            readcsv =csv.reader(csvFile,
                             delimiter=',')
            readcsv = list(readcsv)
            RowNumber = readcsv[self.NumberRow]
        csvFile.close()
        RowNumber.pop(0)
        return RowNumber
    # return data is list by row index 
    def returndatalistrowbyindex (self):
        # get data from conf
        arrlist  = self.ReturnDataAllRowByIndexpath()
        # conver list to string 
        cvstringfromlist = (','.join(arrlist))
        #remove all space 
        cvstringfromlist = cvstringfromlist.strip()
        # return csv from list 
        retl = returnvaluelist(cvstringfromlist,",.(:)",",")
        try:
            retl = [int(i) for i in retl]
        except:
            retl = [str(i) for i in retl]
        return retl

# return data lis trowby index
def returndatalistrowbyindex (path_Cof = None,
                                NumberRow = 0
                                            ):
    csvdata1 = csvdata(path_Cof = path_Cof,
                    NumberRow = NumberRow
                                        )
    return csvdata1.returndatalistrowbyindex()
    
#Return Data All Row By Index path
def ReturnDataAllRowByIndexpath (path_Cof = None,
                                NumberRow = 0
                                            ):
    csvdata1 = csvdata(path_Cof = path_Cof,
                    NumberRow = NumberRow
                                        )
    return csvdata1.ReturnDataAllRowByIndexpath()