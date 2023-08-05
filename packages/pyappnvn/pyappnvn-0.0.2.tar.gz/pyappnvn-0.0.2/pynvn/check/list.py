def check_list_value (valuetocheck = ["None","nhuan"], 
                        checkvalue = [None,""],
                        not_in_checkvalue = True
                        ):
    """ 
    check value in list using all 
    ex1 = valuetocheck = [None,"nhuan"] heckvalue = [None,""] return False,
    ex2 = valuetocheck = ["None","nhuan"] heckvalue = [None,""] return True

    """
    if not_in_checkvalue:
        boresult = all(n not in checkvalue for n in valuetocheck)
    else:
        boresult = any(n in checkvalue for n in valuetocheck)
    return boresult