import csv
from tkinter import messagebox
def convertcsvtolist(path):
    """ convert csv to list """
    with open(path, newline='') as inputfile:
        results = [row[0] for row in csv.reader(inputfile)]
    return results
def convertcsvto1list(path):
    """ convert csv to one list (ex: [1,2,4,53,23]) """
    with open(path, newline='') as inputfile:
        results = list(csv.reader(inputfile))[0]
        if len(results) == 0:
            messagebox.showerror("Error data in csv",
                                "check data in directory path  {0}".format(path))
    return results