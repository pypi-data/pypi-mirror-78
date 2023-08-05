from tkinter import messagebox
from pynvn.excel import colnum_string
def startrow_endrow(ws = None, 
                    rows = [],
                    cols = []
                    ):
    """ 
    Retrieve start row and end row \n
    ws: worksheet input \n
    rows: can be [1], [10,200], []  \n
    if rows = [], return first and last row \n
    """
    if len(rows) == 2:
        return rows
    elif len(rows) == 1:
        return [rows[0],rows[0] + 1]
    elif len(rows) == 0:
        lr = ws.range(colnum_string(cols[0]) +\
            str(ws.cells.last_cell.row)).end('up').row
        return [1,lr + 1]
    else:
        messagebox.showerror("Error",
                             "Not find for this case rows: {0}".format(rows))
