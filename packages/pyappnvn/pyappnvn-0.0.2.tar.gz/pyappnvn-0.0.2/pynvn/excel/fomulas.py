from pynvn.string.slist import str_seplistint_strbystr,returnliststr_from_str,add_sb_to_str
from pynvn.excel import col2num,colnum_string
class vlookup:
    """using function vlookup"""
    def __init__(self,loopkup_value_range = None,
                    table_array = None, 
                    rang_lookup = False, 
                    plexcel = None,
                    colum_to_get_value = None,
                    ws_des = None,
                    Sub_VLOOKUP_Locc_result_value = None,
                    lockrange = True
                    ):
        self.__ws_des = ws_des
        self.__table_array = table_array
        if lockrange:
            self.__table_array = add_sb_to_str(self.__table_array)
        self.__plexcel = plexcel
        self.__rang_lookup = rang_lookup
        self.__loopkup_value_range = loopkup_value_range
        self.__Sub_VLOOKUP_Locc_result_value = Sub_VLOOKUP_Locc_result_value
        self.__cellstart = str_seplistint_strbystr(loopkup_value_range)[0]
        re_value = returnliststr_from_str(table_array)[0]
        self.__cell_start_locvalue = str_seplistint_strbystr(Sub_VLOOKUP_Locc_result_value)[0]
        
        # index column number
        self.__col_index_num = col2num(colum_to_get_value) -  col2num(re_value)  + 1

    def valueformulas(self):

        fomularex = "=IFERROR(VLOOKUP({2},{1}!{0},{3},{4}),{5})".format(self.__table_array,
                                                                    self.__plexcel,
                                                                    self.__cellstart,
                                                                    self.__col_index_num,
                                                                    self.__rang_lookup,
                                                                    '"' + "" + '"'
                                                                    )
        return fomularex
    def forexelldes(self):
        self.__ws_des.range(self.__cell_start_locvalue).value = self.valueformulas()
        vtformulas = self.__ws_des.range(self.__cell_start_locvalue).formula
        self.__ws_des.range(self.__Sub_VLOOKUP_Locc_result_value).formula = vtformulas

class sumif:
    """using function sumif"""

    def __init__(self,sirange = None,
                    sicriteria = None, 
                    sisum_range = None, 
                    plexcel = None,
                    ws_des = None,
                    silrvalue = None,
                    lockrange = True
                    ):
        self.__sirange = sirange
        self.__sicriteria = sicriteria
        self.__sisum_range = sisum_range
        self.__silrvalue = silrvalue
        self.__ws_des = ws_des
        self.__plexcel = plexcel
        self.__cell_start_locvalue = str_seplistint_strbystr(silrvalue)[0]

        if lockrange:
            self.__sirange = add_sb_to_str(self.__sirange)
            self.__sisum_range = add_sb_to_str(self.__sisum_range)

    def valueformulas(self):

        fomularex = "=SUMIF({0}!{1},{2},{0}!{3})".format(self.__plexcel, self.__sirange,self.__sicriteria,self.__sisum_range)

        return fomularex
    def forexelldes(self):
        self.__ws_des.range(self.__cell_start_locvalue).value = self.valueformulas()
        vtformulas = self.__ws_des.range(self.__cell_start_locvalue).formula
        self.__ws_des.range(self.__silrvalue).formula = vtformulas


class anyfun:
    """using function for any function"""

    def __init__(self,function_range = None,
                    function_loc = None,
                    plexcel = None,
                    ws_des = None
                    ):
        self.__function_range = function_range
        self.__function_loc = function_loc
        self.__ws_des = ws_des
        self.__plexcel = plexcel
        self.__cell_start_locvalue = str_seplistint_strbystr(self.__function_loc)[0]

    def forexelldes(self):
        self.__ws_des.range(self.__cell_start_locvalue).value = self.__function_range
        vtformulas = self.__ws_des.range(self.__cell_start_locvalue).formula
        self.__ws_des.range(self.__function_loc).formula = vtformulas