from openpyxl import Workbook
import openpyxl
import xlwings as xw 
from pynvn.excel import mrowandmcolum,sheet_by_namesheet
from pynvn.excel import (convertrangaphatonunber,
                            returnrangelastcolumn)
class credict:
    """ create dict for value and key """
    def __init__ (self, ws = None,
                        rangea = "C7:C1000", 
                        pathfull = None, 
                        namesheet ="PTVT1", 
                        engine ="openpyxl"):
        self.rangea = rangea
        self.engine = engine
        self.ws = sheet_by_namesheet(path=pathfull,
                                        namesheet=namesheet)

        self.lastrow = self.ws.range('A' + str(self.ws.cells.last_cell.row)).end('up').row

        self.rangea = returnrangelastcolumn(stringrang=rangea,lrow=self.lastrow)
    def reindexrownotnone(self):
        """ renturn index which value not none"""
        key_list = [cell.row for cell in self.ws.range(self.rangea) if cell.value != None]
        return key_list

    def revaluerownotnone(self):
        """ renturn value which value not none"""

        value_list = [cell.value for cell in self.ws.range(self.rangea) if cell.value != None]

        return value_list
    def redictvaluesandvaluecol(self, columnumber = 4, removeemtyvalue = True):
        """ return dict value and value column"""
        rnn = self.reindexrownotnone()
        rvm = self.revaluerownotnone()
        arrch = []
        res = list(zip(rnn, rnn[1:] + rnn[:1])) 
        for eler in res:
            arrchild = self.__listchild(eler,columnumber=columnumber)
            arrch.append(arrchild)
            arrchild = None
        dictionary = dict(zip(rvm, arrch))

        if removeemtyvalue:
            new_dict = {key:val for key, val in dictionary.items() if len(val) != 0} 
        else:
            new_dict = dictionary
        return new_dict
    
    def returndictvaluebyindexcolumnandrow(self, 
                                            value_criteria_range, 
                                            range_col ="D7:D1000", 
                                            indexcolumn = [5,6,8]):
        """ return dict by value rangce_col and indexcolumn """
        indexrcevalu = [[self.valuebycol_row(cell.row,indexcolumn[0]),
                                self.valuebycol_row(cell.row,indexcolumn[1]),
                                self.valuebycol_row(cell.row,indexcolumn[2])] \
                                for cell in self.ws.range(range_col) if cell.value == value_criteria_range]

        return indexrcevalu
            
    def valuebycol_row(self,irow,icolumn):
        """ return value cell by index column and row"""
        valuebycolr = self.ws.range(irow,icolumn).value 
        return valuebycolr

    def __listchild(self,ele,columnumber = 4):
        s,t = ele
        arrchild = [[self.ws.range((ie,columnumber)).row,
                        self.ws.range((ie,columnumber)).value] for ie in range(s,t) if self.ws.range((ie,
                                                                                                    columnumber)).value != None] 
        return arrchild

    def listothercell (self,irow,icolumn):
        """ return value of column sheet ptvl1"""
        valuebycolr = self.ws.range(irow,icolumn).value 
        return valuebycolr
