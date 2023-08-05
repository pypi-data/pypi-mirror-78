import xlwings as xw
from pynvn.excel import activesheet,ws_by_namesheet
from pynvn.check.list import check_list_value
from pynvn.error import mssage_error
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

    """ copy and paste range excel to same sheet in file
    """

    sheet_des.range("{0}{1}".format(abccol,
                                    startrow)).value = fomularex
    vtformulas = sheet_des.range("{0}{1}".format(abccol,
                                                startrow)).formula
    sheet_des.range("{0}{1}:{0}{2}".format(abccol,
                                            startrow,
                                            max_row)).formula = vtformulas

def co_paste_move_range(sheet_copy = None,
            range_copy='D:D',
            sheet_des = None,
            range_paste="A1", 
            clear_rcopy_after_copy = True,
            usinglocinexcel = False
            ):
    """ 
    copy and paste range excel to sheet_des
    ex: copy range [A1:C3] of sheet_copy to 
    C5:E20 of sheet_des
    copy to active sheet
    """
    if usinglocinexcel:
        range_copy = sheet_copy.range(self.range_copy).value
        range_paste = sheet_des.range(self.range_paste).value

    if check_list_value(valuetocheck=[range_copy,range_paste]):
        sheet_des.range(range_paste).api.select
        sheet_copy.range(range_copy).api.copy
        sheet_des.api.paste
        # clear or not clear after copy
        if clear_rcopy_after_copy:
            sheet_copy.range(range_copy).clear()
    else:
        mssage_error(cont1=range_copy,cont2=range_paste)            

def cprange_2wb(pathtocopy = None,
            range_copy='D:D',
            sheet_des = None,
            range_paste="A1", 
            clear_rcopy_after_copy = True,
            sheetname_tem = ""
            ):
    """ 
    copy and paste range excel to sheet_des
    ex: copy range [A1:C3] of sheet_copy to 
    C5:E20 of sheet_des
    copy to active sheet
    """

    if check_list_value(valuetocheck=[range_copy,range_paste]):
        sheet_des.range(range_paste).api.select
        wbtocopy = xw.Book(pathtocopy,
                            update_links=False,
                            ignore_read_only_recommended=True,
                            read_only=True)
        sheet_copy = wbtocopy.sheets[sheetname_tem]
        sheet_copy.range(range_copy).api.copy
        sheet_des.api.paste
        # clear or not clear after copy
        if clear_rcopy_after_copy:
            sheet_copy.range(range_copy).clear()
    else:
        mssage_error(cont1=range_copy,cont2=range_paste)   
    wbtocopy.close()
    