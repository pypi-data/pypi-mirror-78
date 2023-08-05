from pynvn.path.ppath import refullpath,getdirpath
from pynvn.string import sepnumberandstrfromstr
from pynvn.string.slist import returnseplistintbbystr,returnlist_from_listinstr
from pynvn.excel import (cellcoordbyvalue,
                        lcellindexbyvalue,
                        col2num,
                        valuebyindexrowcell,
                        returnvaluekeyim,
                        repathlinkexcel,
                        relistsheet,
                        colnum_string,
                        rangecopyrefsamesheet
                        )
from pynvn.csv.tocsv import listtocsvbyarow
from pynvn.csv.tolist import convertcsvto1list
from tkinter import messagebox
class hexcel_sep:
    """copy excel to excel"""
    def __init__(self,wsheet = None,
                    dpath = None,
                    namefile = None,
                    dicrowconf = None,
                    wbnsct = None,
                    pathconf = None
                ):
                self.dicrowconf = dicrowconf
                self.dpath = dpath
                self.wsheet = wsheet
                self.namefile = namefile
                #max colum ws1
                self.mcol = self.wsheet.api.UsedRange.Columns.count
                #max row ws1
                self.mrow = self.wsheet.api.UsedRange.Rows.count
                self.dirpathconf = getdirpath(pathconf)
                self.__hm_rangege = (self.dicrowconf["hm_rangege"])
                self.numberhm = int(sepnumberandstrfromstr(self.__hm_rangege)[1])
                self.__wb1  = wbnsct
                listsheetnamehm = (self.dicrowconf["listsheetnamehm"])
                # return csv have list sheet name 
                self.pathlsn = refullpath(dirpath=self.dirpathconf,
                                        filename=listsheetnamehm)
                try:                        
                    self.lsheet = convertcsvto1list(path=self.pathlsn)
                except:
                    pass
    def habz30 (self):
        """handling data azb-30 sheet"""
        self.__hm_maxrow = int(self.dicrowconf["hm_maxrow"])
        self.__azb30_starcolumn = col2num(self.dicrowconf["azb30_starcolumn"])
        self.__azb30_rowhm = int(self.dicrowconf["azb30_rowhm"])
        self.__azb30_maxrowhm = int(self.dicrowconf["azb30_maxrowhm"])
        self.__azb30_startrowhm = int(self.dicrowconf["zab30_recor_l1"])
        self.__azb30_msa = (self.dicrowconf["azb30_ms"])
        lsheetnamehm = []
        lsheetnames = [sheet.name for sheet in self.__wb1.sheets ]
        for k in range (self.__azb30_starcolumn ,self.mcol):
            hmname =  self.wsheet.range(self.__azb30_rowhm , 
                                        k).value
            if hmname in lsheetnames:
                self.fomuluasfcol(k,hmname=hmname)
                lsheetnamehm.append(hmname)
        # convet to  csv file 
        listtocsvbyarow(listvalue=lsheetnamehm,
                        pathcsv=self.pathlsn )

    def fomuluasfcol (self,k,hmname = None ):
        """fomulas for column follow index"""
        pfile = repathlinkexcel(dpath=self.dpath,
                                namefile=self.namefile,
                                namesheet=hmname)
                                
        valueim = returnlist_from_listinstr(self.dicrowconf["zab30_valueim"].replace(":", ","))
        if len(valueim) != 0: 
            lindexrow_im = lcellindexbyvalue(max_row=self.mrow,
                                                min_row=self.__azb30_startrowhm,
                                                max_col=self.__azb30_msa,
                                                min_col=self.__azb30_msa,
                                                sheet=self.wsheet,
                                                lvalue=valueim
                                                )
        
            lvaluebyindecell_im = valuebyindexrowcell(lindexcell=lindexrow_im,
                                                    col=colnum_string(k),
                                                    sheet=self.wsheet)

        valueformulas = "=SUMIFS({0}!$L${4}:$L${3},{0}!$B${4}:$B${3},C{2})".format(pfile,
                                                                                    "'" + "AZB-30" + "'",
                                                                                    self.__azb30_startrowhm,
                                                                                    self.__hm_maxrow ,
                                                                                    self.numberhm
                                                                                    )

        rangecopyrefsamesheet(sheet=self.wsheet,
                            formulasfirstcell=valueformulas,
                            col_index=k,
                            startrow=self.__azb30_startrowhm,
                            endrow=self.__azb30_maxrowhm)
        if len (valueim) != 0: 
            returnvaluekeyim(cola=colnum_string(k),
                            listvalue_im=lvaluebyindecell_im,
                            sheet=self.wsheet,
                            indexrow_im=lindexrow_im
                            )
    def habz60 (self):
        """handling data azb-60 sheet"""
        col_msa = (self.dicrowconf["azb60_ms"])
        startrowhm = int(self.dicrowconf["zab60_recor_l1"])
        dongia = col2num(self.dicrowconf["azb60_dongia"])
        dongia_abc = self.dicrowconf["azb60_dongia"]
        rangeketcauthep = (self.dicrowconf["azb60_rangeketcauthep"])
        valueim = returnlist_from_listinstr(self.dicrowconf["zab60_valueim"].replace(":", ","))
        m_row = self.wsheet.range(col_msa + str(self.wsheet.cells.last_cell.row)).end('up').row
        # return index row by value
        if len (valueim) != 0: 
            lindexrow_im = lcellindexbyvalue(max_row=self.mrow,
                                                min_row=startrowhm,
                                                max_col=col_msa,
                                                min_col=col_msa,
                                                sheet=self.wsheet,
                                                lvalue=valueim
                                                )
        
            lvaluebyindecell_im = valuebyindexrowcell(lindexcell=lindexrow_im,
                                                    col=dongia_abc,
                                                    sheet=self.wsheet)

        # return range number
        rangese= returnseplistintbbystr(strint=rangeketcauthep)

        sumvalue = "=" + self.__returnsumvalue(iden="other",
                                        startrow60=startrowhm)

        rangecopyrefsamesheet(sheet=self.wsheet,
                            formulasfirstcell=sumvalue,
                            col_index=dongia,
                            startrow=startrowhm,
                            endrow=m_row)

        # rewwrite ket cau thep 
        sumvalue = "=" +  self.__returnsumvalue(iden="kct",
                                        startrow60=rangese[0])
        
        rangecopyrefsamesheet(sheet=self.wsheet,
                                formulasfirstcell=sumvalue,
                                col_index=dongia,
                                startrow=rangese[0],
                                endrow=rangese[1])
        if len (valueim) != 0: 
            returnvaluekeyim(cola=dongia_abc,
                            listvalue_im=lvaluebyindecell_im,
                            sheet=self.wsheet,
                            indexrow_im=lindexrow_im
                            )
  
    def __returnsumvalue (self,iden ="kct", startrow60 = 100):
        # list all sheet name from file path 
        sumvalue = ""
        for hmname in self.lsheet:

            valuesum = self.__valuecolsheet(i = startrow60,
                                            hmname=hmname,iden=iden)
            sumvalue = sumvalue + "+" +  valuesum        
        return sumvalue

    def __valuecolsheet (self,i = 1,hmname = None, iden = "kct"):
        """fomulas for column follow index"""
        pfile = repathlinkexcel(dpath=self.dpath,
                                namefile=self.namefile,
                                namesheet=hmname
                                )
        if iden != "kct":
            valueeee = 'SUMIF({0}!$BC:$BC,C{1},{0}!$CA:$CA) + SUMIF({0}!$BC:$BC,C{1},{0}!$CB:$CB)'.format(pfile,i)
        else:
            valueeee = 'SUMIF({0}!$BC:$BC,C{1},{0}!$CC:$CC) + SUMIF({0}!$BC:$BC,C{1},{0}!$CD:$CD)'.format(pfile,i)
        return valueeee

    def returnlistvaluebycolumnindex (self):

        return [cell.value for row in ws.iter_rows('C{}:C{}'.format(ws.min_row,ws.max_row)) for cell in row]
    def azb50(self):
        #='C:\Users\HP\Desktop\test\[KE HOACH NGAN SACH.xlsx]B3-Factory'!$BX$7
        startrowhm = int(self.dicrowconf["zab50_recor_l1"])
        maythicong_col =col2num(self.dicrowconf["azb50_hm"])
        dongia = self.dicrowconf["azb50_dongia"]
        dongia_int = col2num(dongia)
        colmay_nc = self.dicrowconf["azb50_colmay_nc"]
        colmay_nc_row = int(self.dicrowconf["azb50_colmay_nc_row"])

        crow = startrowhm + 1
        for sheetn in self.lsheet:
            self.wsheet.range(crow,maythicong_col).value = sheetn
            
            pfile = repathlinkexcel(dpath=self.dpath,
                                    namefile=self.namefile,
                                    namesheet=sheetn
                                    )
            self.wsheet.range(crow,dongia_int).value  = "={0}!${1}${2}".format(pfile,
                                                                            colmay_nc,
                                                                            colmay_nc_row)
            crow = crow + 1
    def azb40(self):
        startrowhm = int(self.dicrowconf["zab40_recor_l1"])
        maythicong_col =col2num(self.dicrowconf["azb40_hm"])
        dongia = self.dicrowconf["azb40_dongia"]
        dongia_int = col2num(dongia)
        colmay_nc = self.dicrowconf["azb40_colmay_nc"]
        colmay_nc_row = int(self.dicrowconf["azb40_colmay_nc_row"])
        crow = startrowhm + 1
        for sheetn in self.lsheet:
            self.wsheet.range(crow,maythicong_col).value = sheetn
            
            pfile = repathlinkexcel(dpath=self.dpath,
                                    namefile=self.namefile,
                                    namesheet=sheetn
                                    )
            self.wsheet.range(crow,dongia_int).value  = "={0}!${1}${2}".format(pfile,
                                                                            colmay_nc,
                                                                            colmay_nc_row)
            crow = crow + 1
    def itemiden(self):
        """item identification"""
        self.__azb30_starcolumn = col2num(self.dicrowconf["azb30_starcolumn"])
        self.__azb30_rowhm = int(self.dicrowconf["azb30_rowhm"])
        #lsheetnamehm = []
        lsheetnames = [sheet.name for sheet in self.__wb1.sheets ]
        lsheetnamehm = [self.wsheet.range(self.__azb30_rowhm , k).value  \
                        for k in range (self.__azb30_starcolumn ,self.mcol) \
                        if self.wsheet.range(self.__azb30_rowhm , k).value in lsheetnames]
        if len(lsheetnamehm) == 0:
            messagebox.showerror("Error", "Review {0}, has it processed?".format("AZB-30"))
        # convet to  csv file 
        listtocsvbyarow(listvalue=lsheetnamehm,
                        pathcsv=self.pathlsn )