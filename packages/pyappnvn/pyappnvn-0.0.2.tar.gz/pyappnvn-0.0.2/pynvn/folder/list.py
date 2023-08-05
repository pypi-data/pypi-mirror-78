import os
from pynvn.path.ppath import dirfolder
def listfileofpfolder(folderchild, fmnamefile = ["jpg","gif"]):
    """ return list file of p folder"""
    os.chdir(folderchild)
    lfiles = os.listdir(folderchild)
    lfileinforders = [lfile for lfile in lfiles if any(n in lfile for n in fmnamefile)]
    return lfileinforders
def file_in_folder(path):
    """ return list file in folder"""
    try: 
        os.chdir(path)
        # list file  excel 
        return os.listdir(path)
    except:
        messagebox.showerror ("Error","check for folder path {}".format(path))
def file_in_folders(paths = []):
    """ return list file in folders """
    flist = []
    for path in paths:
        elist = file_in_folder(path)
        flist = flist + elist
    return flist

def ldirfolders(dirNamec = None, 
                lsubforders = [],
                alertexists = True
                ):
    """ return list dir folders """
    return [dirfolder(dirNamec=dirNamec,subforder=subf,alertexists=alertexists) for subf in lsubforders]