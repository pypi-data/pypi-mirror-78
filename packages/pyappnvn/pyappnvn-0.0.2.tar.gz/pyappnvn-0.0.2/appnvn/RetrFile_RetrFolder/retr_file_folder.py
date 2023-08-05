from pynvn.csv.todict import dictfromcsv2col_evallist
from pynvn.excel import activesheet,listsheet_by_wb
from pynvn.list.flist import filterlistbylstr
from pynvn.path.ppath import refullpath
from appnvn.exazp.excel.hchildsheet import hchildsheet
import xlwings as xw
class rapp:
    """ fill the formulas into excel file """
    def __init__(self,path_des = None,
                    path_copy_dir = None,
                    fuction = None,
                    pathconf = None,
                    lsheet_ex = []
                    ):
        self.__path_copy_dir = path_copy_dir
        self.__lsheet_ex = lsheet_ex
        self.__dictconf = dictfromcsv2col_evallist(path=pathconf)
        self.__fuction = str(fuction).lower()         
        self.__app = xw.App(visible=True,
                            add_book=False
                            )
        self.__desxw = self.__app.books.open(fullname=path_des,
                                            update_links=False)
    def ft_tool(self):
        lfuns = filterlistbylstr(liststr=list(self.__dictconf.keys()),
                                criteria_is_not=True,
                                criteria=["sub_"],
                                upper = False
                                )
        mydictfun = {
                    "transfertoparent":(lambda: self.__transfertoparent()),
                    "transfertoparents":(lambda: self.__transfertoparents())
                    }
        if self.__fuction == "config":
            for lfun in lfuns:
                mydictfun[lfun]()
        else:
             mydictfun[self.__fuction]()
    def __transfertoparent(self):
        lsheet =  self.__dictconf["sub_transfertoparent_listsheetname"]
        for name_ele_ex in self.__lsheet_ex:
            path_copy = refullpath(dirpath=self.__path_copy_dir,
                                    filename = name_ele_ex
                                    )
            copyxw = self.__app.books.open(fullname=path_copy ,
                                            update_links=False,                       
                                            read_only=False,
                                            ignore_read_only_recommended=False
                                            )
            ws_copy = retrive_sname_sheet(copyxw=copyxw,
                                            desxw=self.__desxw,
                                            lsheet=lsheet
                                            )   
            # check ws_copy 
            if ws_copy == None:continue
            # retrive parameter from file excel config
            yerorno = self.__dictconf["transfertoparent"]
            nstart_row = int(self.__dictconf["sub_transfertoparent_recor_l1"])
            valueim = self.__dictconf["sub_transfertoparent_valueim"]
            msstr =self.__dictconf["sub_transfertoparent_ms"]
            for_using_loc = self.__dictconf["sub_transfertoparent_forbydup"]
            loc_use_formulas = self.__dictconf["sub_transfertoparent_locuseformulas"]
            col_dup = self.__dictconf["sub_transfertoparent_dup"]
            # retrive sheet des and active
            self.__desxw.sheets[ws_copy.name].activate()
            ws_des = activesheet() 
            hchildsheet(startrow=nstart_row,
                        col_key_msa=msstr,
                        lcolumnformulas = loc_use_formulas,
                        valueim=valueim,
                        sheet_des =activesheet(),
                        sheet_copy=ws_copy,
                        col_dup=col_dup,
                        formulasfor_col_dup = for_using_loc
                        ) if yerorno == "yes" else False

            copyxw.close()
        self.__desxw.save()
        self.__desxw.close()
        self.__app.quit()            
    def __transfertoparents(self):
        for name_ele_ex in self.__lsheet_ex:
            path_copy = refullpath(dirpath=self.__path_copy_dir,
                                    filename = name_ele_ex
                                    )
            copyxw = self.__app.books.open(fullname=path_copy ,
                                                update_links=False,                       
                                                read_only=False,
                                                ignore_read_only_recommended=False
                                                )

            lkeys = list(self.__dictconf.keys())
            # lengh of sheet name key 
            llen= len("sub_transfertoparents_namesheet")
            key_snames = [lkey[llen:] for lkey in lkeys if "sub_transfertoparents_namesheet" in lkey]
            yerorno = self.__dictconf["transfertoparents"]
            for key_sname in key_snames:
                sheetname = self.__dictconf["sub_transfertoparents_namesheet" + key_sname]
                nstart_row = int(self.__dictconf["sub_transfertoparents_recor_l1" + key_sname])
                valueim = self.__dictconf["sub_transfertoparents_valueim" + key_sname]
                msstr =self.__dictconf["sub_transfertoparents_ms" + key_sname ]
                for_using_loc = self.__dictconf["sub_transfertoparents_forbydup" + key_sname]
                loc_use_formulas = self.__dictconf["sub_transfertoparents_locuseformulas" + key_sname]
                col_dup = self.__dictconf["sub_transfertoparents_dup" + key_sname]
                ws_copy = retrive_sname_sheet(copyxw=copyxw,
                                                desxw=self.__desxw,
                                                lsheet=[sheetname]
                                                )     
                # check ws_copy 
                if ws_copy == None:continue
                # retrive sheet des and active
                self.__desxw.sheets[ws_copy.name].activate()
                # transer range  using VLOOLUP
                hchildsheet(startrow=nstart_row,
                            col_key_msa=msstr,
                            lcolumnformulas = loc_use_formulas,
                            valueim=valueim,
                            sheet_des =activesheet(),
                            sheet_copy=ws_copy,
                            col_dup=col_dup,
                            formulasfor_col_dup = for_using_loc
                            ) if yerorno == "yes" else False
            copyxw.close()
        self.__desxw.save()
        self.__desxw.close()
        self.__app.quit() 
def retrive_sname_sheet(copyxw,desxw,lsheet):
    """ retrive sheet copy from sheet copy and sheet des"""
    for sheet in copyxw.sheets:
        if (sheet.name in lsheet and sheet.name in listsheet_by_wb(desxw)) :
            return sheet
            break