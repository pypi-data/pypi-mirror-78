from tkinter import messagebox
import os
import shutil
from pynvn.path.ppath import listfileinfolder
def listfolderofpfolder(folderchild):
    """ return list folder of parent folder"""
    os.chdir(folderchild)
    try:
        lfolderp = os.listdir(folderchild)
    except:
        messagebox.showerror ("Error"," No folder parent folder: {}".format(folderchild))
    return lfolderp
def remove_folder(path):
    """ remove folder of path"""
    # check if folder exists
    if os.path.exists(path):
         # remove if exists
         shutil.rmtree(path,ignore_errors=False)
    else:
         # throw your exception to handle this special scenario
         raise XXError("your exception") 