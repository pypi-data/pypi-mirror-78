from pynvn import dict_from_csv2col
def hfunction(lfun, pathconf):
    dictconf = dict_from_csv2col(pathconf)
        if lfun == "move_range":
            mrange = dictconf["move_range"]
            Value_Conf_Loc = dictconf["sub_move_range_value_conf_Loc"]
            sheet_name = dictconf["sub_sheetname"]
            range_copy = dictconf["sub_range_copy"]
            range_des = dictconf["sub_range_des"]
            if mrange =="yes":
                if sheet_name == "active":
                    co_paste_move_range(sheet_copy=acsheet,
                                        sheet_des=acsheet
                                        )           
    