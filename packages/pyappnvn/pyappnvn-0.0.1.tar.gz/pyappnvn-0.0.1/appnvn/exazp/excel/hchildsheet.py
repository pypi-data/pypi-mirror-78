from pynvn.excel import (cellcoordbyvalue,
                        lcellindexbyvalue,
                        col2num,
                        valuebyindexrowcell,
                        colnum_string,
                        repathlinkexcel
                        )
from pynvn.path.ppath import getdirpath,ExtractFileNameFromPath


class hchildsheet:
    """ 
    retreve data at from sheet child using vlookup.
    note: sheet_des must active.
    startrow: row start in sheet_copy.
    col_key_msa: The value to look for in the first column of a table.
    lcolumnformulas: column_index to using vlookup.
    """
    def __init__(self,
                startrow = 1,
                col_key_msa = None,
                lcolumnformulas = None, 
                valueim = None,
                sheet_des = None,
                sheet_copy = None, 
                col_dup = None,
                lvaluehavechild = [],
                formulasfor_col_dup = None
                ):
        self.__startrow = startrow
        self.__col_key_msa = col_key_msa
        # retrive full name of sheet_coy
        psheet_copy = sheet_copy.book.fullname
        # retrive dir path of sheet _copy
        dirp_sheet_copy = getdirpath(psheet_copy)
        # retrive file name of des copy 
        filename_sheet_copy  = ExtractFileNameFromPath(path=psheet_copy)
        # # retrive path link using for formulas 
        self.__pfile = repathlinkexcel(dpath=dirp_sheet_copy,
                                        namefile=filename_sheet_copy,
                                        namesheet=sheet_copy.name
                                        )
        self.__columnlra = [colnum_string(1),colnum_string(sheet_copy.api.UsedRange.Columns.count)]
        self.__max_row = sheet_des.range(col_key_msa + str(sheet_des.cells.last_cell.row)).end('up').row
        self.__lcolumnformulas = lcolumnformulas
        self.__valueim = valueim
        self.__sheet_des = sheet_des
        self.__sheet_copy = sheet_copy
        self.__lvaluehavechild = lvaluehavechild
        self.__max_row_allsheet = sheet_copy.api.UsedRange.Rows.count
        self.__formulasfor_col_dup = formulasfor_col_dup
        self.__col_dup = col_dup
        if len (self.__valueim) != 0:
            self.lindexrow_im = lcellindexbyvalue(max_row=self.__max_row_allsheet,
                                                min_row=self.__startrow,
                                                max_col=self.__col_key_msa,
                                                min_col=self.__col_key_msa,
                                                sheet=self.__sheet_des,
                                                lvalue=self.__valueim
                                                )
        self.tranderdatasheettosheet()
        if len(self.__col_dup) !=0:
            self.hdataatdupcolumn()
    def tranderdatasheettosheet(self):
        """ transfer data formulas to another sheet """
        for abccol in self.__lcolumnformulas:
            if len (self.__valueim) != 0: 
                lvaluebyindecell_im = valuebyindexrowcell(lindexcell=self.lindexrow_im,
                                                        	col=abccol,
                                                            sheet=self.__sheet_des)
            indexcol = col2num(abccol) -  col2num(self.__col_key_msa)  + 1
            fomularex = "=IFERROR(VLOOKUP({1}{0},{2}!${1}${0}:${4}${6},{7},FALSE),{8})".format(self.__startrow,
                                                                                        self.__col_key_msa,
                                                                                        self.__pfile,
                                                                                        self.__col_key_msa,
                                                                                        self.__columnlra[1],
                                                                                        self.__startrow,
                                                                                        self.__max_row_allsheet,
                                                                                        indexcol,
                                                                                        '"' + "" + '"'
                                                                                        )
            self.__sheet_des.range("{0}{1}".format(abccol,
                                                    self.__startrow)).value = fomularex
            vtformulas = self.__sheet_des.range("{0}{1}".format(abccol,
                                                    self.__startrow)).formula


            self.__sheet_des.range("{0}{1}:{0}{2}".format(abccol,
                                                        self.__startrow,
                                                        self.__max_row)).formula = vtformulas
            if len (self.__valueim) != 0: 
                self.returnvaluekeyim(cola=abccol,listvalue_im =lvaluebyindecell_im)
    def returnvaluekeyim (self,cola,listvalue_im):
        """ return value at key value from sheet copy to sheet des """
        for count,numberint in enumerate(self.lindexrow_im,0):
            self.__sheet_des.range("{0}{1}".format(cola,
                                                    numberint)).value = listvalue_im[count]
    def hdataatdupcolumn(self):
        """ h data at column index """
        for count,eles in enumerate(self.__col_dup,0):
            if len(self.__lvaluehavechild) != 0:
                lindexrow = lcellindexbyvalue(max_row=self.__max_row_allsheet,
                                            min_row=self.__startrow,
                                            max_col=self.__col_key_msa,
                                            min_col=self.__col_key_msa,
                                            sheet=self.__sheet_des,
                                            lvalue=self.__lvaluehavechild
                                            )
                for index in lindexrow:
                    self.__sheet_des.range("{0}{1}".format(eles,index)).formula = self.__formulasfor_col_dup[count].format(index)
            else:
                if len (self.__valueim) != 0: 
                    lvaluebyindecell_im = valuebyindexrowcell(lindexcell=self.lindexrow_im,
                                                            col=eles,
                                                            sheet=self.__sheet_des
                                                            )

                self.__sheet_des.range("{0}{1}".format(eles,
                                                        self.__startrow)).value = self.__formulasfor_col_dup[count].format(self.__startrow)

                vtformulas = self.__sheet_des.range("{0}{1}".format(eles,self.__startrow)).formula

                self.__sheet_des.range("{0}{1}:{0}{2}".format(eles,
                                                self.__startrow,
                                                self.__max_row)).formula = vtformulas
                if len (self.__valueim) != 0: 
                    self.returnvaluekeyim(cola=eles,listvalue_im =lvaluebyindecell_im)
            