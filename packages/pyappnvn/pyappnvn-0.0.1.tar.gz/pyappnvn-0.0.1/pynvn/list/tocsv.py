import csv
from pynvn.string import no_accent_vietnamese
def listocsvhor(pathtow = None,listv = None):
    """ convert list to csv horizontal """
    with open(pathtow, 'w') as csvFile:
        wr = csv.writer(csvFile,lineterminator='\n')
        wr.writerow(listv)
    csvFile.close()

def listocsvver(pathtow = None,listv = None):
    """ convert list to csv vertival """
    with open(pathtow, "w") as f:
        writer = csv.writer(f,lineterminator='\n')
        for row in listv:
            row = no_accent_vietnamese(row)
            writer.writerow([row])