import csv
class rcsv:
    """ read csv """
    def  __init__(self, pathtor = None,
                        NumberRow = 1,
                        indexarrtoget = [0,1] ) :
        self.pathtor = pathtor
        self.NumberRow = NumberRow
        self.indexarrtoget = indexarrtoget

    
    def CountNumberOfRow (self):
        """ count number of row in csv """
        with open(self.pathtor, 'r') as readFile:
            a = sum (1 for row in readFile)
        readFile.close
        return a
    
    def Redtallrowbyindxaindexarr (self):
        """ return all value in row by index """
        newRowNumber = []
        with open(self.pathtor,"r") as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            readcsv = list(readcsv)
            RowNumber = readcsv[self.NumberRow]
            newRowNumber = [RowNumber[ind] for ind in self.indexarrtoget]
        csvFile.close()
        return newRowNumber 

    
    def Redtallrowbyindxaindexarrall (self):
        """ return all value of all row """
        Reall = []
        recount = self.CountNumberOfRow()
        for count in range (recount):
            self.NumberRow = count
            Reall.append(self.Redtallrowbyindxaindexarr())
        return Reall

    
    def Rerowbyindxaindexarr (self):
        """ return all row follow index """
        newRowNumber = []
        with open(self.pathtor,"r") as csvFile:
                readcsv =csv.reader(csvFile, delimiter=',')
                recount = self.CountNumberOfRow()
                for count in range (recount):
                    self.NumberRow = count
                    readcsv = list(readcsv)
                    RowNumber = readcsv[self.NumberRow]
                    newRowNumber.append(RowNumber[self.indexarrtoget[0]])
        csvFile.close()
        return newRowNumber 
    
def returndictrowforcsv (path):
    """ count number of row in csv """
    with open(path, 'r') as readFile:
        listk = {lcsv[0]:lcsv[1] for lcsv in list(csv.reader(readFile, delimiter=','))}
    return listk


