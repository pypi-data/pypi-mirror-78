from tkinter import messagebox
from pynvn.list.str import exstrtolistint
def returnlistfolderbywh(foldernamelist,
                        width_p,
                        height_p):
    """ return list folder by w and h """
    listfolder = [folderch for folderch in foldernamelist if \
                (exstrtolistint (folderch)[0] <= width_p) and\
                ((exstrtolistint (folderch)[1]) <= height_p)]
    if len (listfolder) ==0:
        messagebox.showerror ("error","list folder is empty in folder \n \
                                parent {0} with width is {1} and height is {2} ".format(foldernamelist,
                                                                                        width_p,
                                                                                        height_p))
    else:
        return listfolder 