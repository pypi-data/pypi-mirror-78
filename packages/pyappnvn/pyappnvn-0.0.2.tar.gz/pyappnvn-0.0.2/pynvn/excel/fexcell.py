#  write to excel 
import pandas as pd
from pynvn.path import (
                            returndatalistrowbyindex
                            )
from pynvn.data import grouper

class toexcel:
    def __init__(self,worksheet = None,
                             path = None, 
                             value = None,
                             path_conf = None,
                             lpath = None,
                             rpath = None,
                             loccelpath = 29
                             ):

        self.worksheet = worksheet
        self.value = value
        self.path = path
        self.path_conf = path_conf
        self.lpath = lpath
        self.rpath = rpath
        self.loccelpath = loccelpath

    """
    write path to location of excel 
    using path config to find address of cell
    """

    def reloccol (self):

        locpath = returndatalistrowbyindex(self.path_conf,
                                          self.loccelpath)
        # group to pair arr 
        locpath =  list(grouper(2,locpath))
        # check left and rignt to fill out to excel 
        if self.path == self.lpath:
            loc_col =  locpath[0]
        else:
            loc_col =  locpath[1]
        # convert type arr to int
        loc_col = [int(i) for i in loc_col]
        # fill out title to excel
        return loc_col
    # write move column to excel 

    def writemovecol (self,loccolmove,
                            colmove):
        loccolmove =  list(grouper(2,loccolmove))
        for cell,index in zip(loccolmove,
                                colmove):

            df = pd.read_csv(self.path,
                             delimiter=',',
                             index_col = None ,
                             usecols = [index],
                             nrows= 1)
            # convert type arr to int
            self.worksheet.cell(row = cell[0], 
                                column = cell[1]).value = df.iat[0,0]
    # write value to excell 
    def wrivaltoexc (self):
        loc_col = self.reloccol()
        self.worksheet.cell(row = loc_col[0],
                            column = loc_col[1]).value = "Path CSV"
        # fill out value path to excel 
        self.worksheet.cell(row = loc_col[0],
                            column = (int(loc_col[1]) + 1)).value = self.path
