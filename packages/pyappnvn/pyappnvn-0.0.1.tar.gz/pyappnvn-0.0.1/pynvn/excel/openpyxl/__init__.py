from pynvn.excel import col2num   
import openpyxl
def returnloccellbyvalue(path = None ,min_row = 1,max_row=100,min_col=3,max_col=3,valuetofind = 1200, namesheet = None):
    """ return location of cell (row index and column index) ---->[cell.row,cell.column]"""
    if type(min_col) == str:
        min_col = col2num(min_col)
    if type(max_col) == str:
        max_col = col2num(max_col)
    wb = openpyxl.load_workbook(path, 
                                read_only=True)
    ws = wb[namesheet]
    for row in ws.iter_rows(min_row = min_row,
                            max_row=max_row,
                            min_col=min_col,
                            max_col=max_col):
        for cell in row:
            if str(cell.value) == str(valuetofind):
                return [cell.row,cell.column] #change column number for any cell value you wants