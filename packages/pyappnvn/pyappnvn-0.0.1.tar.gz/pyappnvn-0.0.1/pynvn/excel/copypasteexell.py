import xlwings as xw
def cprange(pathtocopy = None,
            rangetocopy='BB5:CF100',
            pathtodes = None,
            rangetopaste="BB5", 
            namesheettocopy ='sheet_config' 
            ):

    """ 
    copy and paste range excel to another file
    ex: copy range [A1:C3] of pathtocopy to 
    C5:E20 of pathtodes
    copy to active sheet
    """
    pathtodes.range(rangetopaste).api.select
    wbtocopy = xw.Book(pathtocopy)
    sheet_copy = wbtocopy.sheets[namesheettocopy]
    sheet_copy.range(rangetocopy).api.copy
    pathtodes.api.paste
    # not cut excel 
    wbtocopy.app.api.CutCopyMode=False
    wbtocopy.close()
def cprangesamesheet(sheet = None,
                    rangetocopy='BB5:CF100',
                    rangetopaste="BB5"
                    ):

    """ 
    copy and paste range excel to same sheet in file
    """

    sheet_des.range("{0}{1}".format(abccol,
                                    startrow)).value = fomularex
    vtformulas = sheet_des.range("{0}{1}".format(abccol,
                                                startrow)).formula
    sheet_des.range("{0}{1}:{0}{2}".format(abccol,
                                            startrow,
                                            max_row)).formula = vtformulas
