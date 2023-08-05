import os
from tkinter import Entry

class namefile:
    def  __init__(self, dirpath = None,
                        fnamesub = None
                ):
        self.dirpath = dirpath
        self.fnamesub = fnamesub
    def returnallfilenameinfolder(self):
        entries = os.listdir(self.dirpath)
        return entries
    def returnfilfullnamefromsubname(self):
        entries = self.returnallfilenameinfolder()
        for etry in entries:
            if self.fnamesub in etry:
                return etry
        else:
            print ("can not find file")
            
        