import os
import csv
import sys
from tkinter import messagebox,filedialog
import tkinter as tk
import openpyxl as xl


def check_pfile(cpath,title = "Error directory"):
    """ check directory of path """
    if cpath:
        pass
    else:
        messagebox.showerror("Error directory","Check {0} again".format(cpath))

class PathSteel:
    def  __init__(self, path_Full = None,
                        dir_path = None,
                        Is_Directory_Path_To_SubFolder = False,
                        Path_Conf = None,
                        FileName = None,
                        modulename = None,
                        pathorigrn = None,
                        pathdestination = None,
                        subfolder = None
                    ):
            self.path_Full = path_Full
            self.dir_path = dir_path
            self.Path_Conf = Path_Conf
            self.Is_Directory_Path_To_SubFolder =\
                 Is_Directory_Path_To_SubFolder
            self.FileName = FileName
            self.modulename = modulename
            self.pathorigrn = pathorigrn
            self.pathdestination = pathdestination
            self.subfolder = subfolder

    def resource_path_is_from_pyinstall_and_dev(self):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, self.FileName)

    def ExtractFileNameFromPath (self):
        """function to get faname from fullpath """
        # get file Name
        try:
            FileName = os.path.basename(self.path_Full)
        except AttributeError as error:
            print (error)
        return FileName
 
    def refpath(self,args = None):
        """Return full path conbine subfolder"""
        # check directory path is to subfolder or not ?
        if self.Is_Directory_Path_To_SubFolder == True:
            #unpack to get element in list
            #join 2 folder together 
            dir_path = os.path.join(self.dir_path,
                                            self.subfolder)
                
            # Concatenate folder and file name 
            full_path = os.path.join(dir_path,
                                    self.FileName)
        else:
            # Create full path
            full_path = os.path.join(self.dir_path,
                                    self.FileName)
            if os.path.exists(full_path) == False:
                file = open(full_path, 'w+')
        return full_path

    def getpathmodule (self):
        """ get path of module was imported """
        pathf = os.path.join((os.path.dirname(self.modulename.__file__)),
                                                self.FileName)
        return pathf
    def saveasfiletopathAndopen (self):
        # get file name from path 
        filename = ExtractFileNameFromPath(self.pathorigrn)
        wb1 = xl.load_workbook(self.pathorigrn)
        #save excel to ative folder
        try:
            wb1.save(filename)
            os.system('start "excel" {}'.format(filename))
        except:
            messagebox.showerror("Error","File name: {} is openning, close file to continue ".format(filename))
    @property
    def subfolder(self):
        return self.__subfolder
    @subfolder.setter
    def subfolder(self,newfolder):
        self.__subfolder = newfolder
    
    @property
    def FileName(self):
        return self.__FileName
    @FileName.setter
    def FileName(self,newname):
        self.__FileName = newname
    
def resource_path_is_from_pyinstall_and_dev (FileName = None,
                                             Subfolder = None ,
                                             Is_Directory_Path_To_SubFolder = False,
                                             dir_path = None
                                            ):
    """using function to return resourse path"""

    PathS = PathSteel(FileName = FileName,
                        Is_Directory_Path_To_SubFolder = Is_Directory_Path_To_SubFolder,
                        dir_path = dir_path
                    )
    return PathS.refpath(Subfolder)

def ExtractFileNameFromPath(path = None):
    """Get file name from path full
        ex:  \\folder\\nhuan.xlsx ---> nhuan.xlsx
    """
    PathS = PathSteel(path_Full = path) 
    return PathS.ExtractFileNameFromPath()

 
def IsRunningInPyinstallerBundle ():
    """running in a PyInstaller bundle or running in a normal Python process"""
    try:
        if getattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
            return True
    except:
        return False

def PathFromFileNameAndDirpath (dir_path = None, 
                                filename = None):
    """get Path full from directory path and file name"""

    PathS = PathSteel(dir_path = dir_path,
                        FileName = filename
                    )
    full_path = PathS.refpath()
    return full_path

def getpathfromtk(outputpath = None,Warning_path_existing = True):
    """ get content entry from output for tk widget"""
    if os.path.exists(outputpath.get()):
        return outputpath.get()
    else: 
        messagebox.showinfo("Directory", "Directory not found for option") if  Warning_path_existing else False

def retabspath():
    """ return dir path folder """
    return os.path.dirname(os.path.abspath(__file__))
    
def abspath(Balance_Stock):
    return os.path.abspath(Balance_Stock)

def getdirpath(pathfull):
    """ get dir path from path full """
    return os.path.dirname(pathfull)

def getfilenamewoexten (filenameinstension):
    """ extract file name from file name """
    filename, file_extension = os.path.splitext(filenameinstension)
    return filename

def parentdirectory (path):
    """ get dir path from path full """
    return os.path.dirname (path)

def credirfol (dirNamec, subforder):
    """ create dir folder """
    try:
        dirName = os.makedirs(os.path.join(dirNamec, subforder))
    except:
        messagebox.showerror ("Error","{} already exists".format(subforder))
    return os.path.join(dirNamec, subforder)

def refullpath(dirpath, 
                filename, 
                folderchild = None, 
                createfilenameifnotexsting = True,
                createfolderifnotexsting = True):
    """ return full name from dir folder and finame name"""
    if folderchild == None:
        fpath = os.path.join(dirpath, filename)
        if os.path.exists(fpath) == False:
            open(fpath, 'w') if createfilenameifnotexsting else messagebox.showerror("name file error", 
                                                                                        "Check filename {0} in folder directory {1} not exsting  ".format(filename,
                                                                                                                                                            dirpath))
        return fpath
    else:
        if createfolderifnotexsting:
            fpathc = repathfolderchild(dirpath=dirpath,
                                            subFolder=folderchild,
                                            createfolderifnotexsting= True
                                         )
        else:
            fpathc = repathfolderchild(dirpath=dirpath,
                                            subFolder=folderchild,
                                            createfolderifnotexsting= False
                                            )
        fpath = os.path.join(fpathc, filename)
        if os.path.exists(fpath) == False:
                 open(fpath, 'w') if createfilenameifnotexsting else messagebox.showerror("name file error", 
                                                                                        "Check filename {0} in folder directory {1} not exsting  ".format(filename,
                                                                                                                                                            dirpath))
        return fpath
def repathfolderchild(dirpath, 
                        subFolder, 
                        createfolderifnotexsting = True
                        ):
    """ return path folder child from dir path and sub folder """
    path = os.path.join(dirpath,subFolder)
    if os.path.exists(path):
        return path
    else: 
        if createfolderifnotexsting:
            return credirfol(dirNamec=dirpath,subforder= subFolder)
        else:
             messagebox.showerror ("folder", "folder name {0} in path parent {1} not exists".format(subFolder,dirpath))

def resource_path_is_from_pyinstall_and_dev(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
    except Exception:
            base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def listfileinfolder(path):
    """ return list file in folder"""
    try: 
        os.chdir(path)
        # list file  excel 
        return os.listdir(path)
    except:
        messagebox.showerror ("Error","check for folder path {}".format(path))

def mfileopen(outputtk, 
                file_open = True):
        """ open file parent"""
        outputtk.delete(0, 'end')
        if file_open:
            # ask directory file
            files = filedialog.askopenfilename(title = "Directory of parent file",
                                                initialdir=outputtk.get())

            outputtk.insert(tk.END,files)

        else:
            # ask directory folder
            files = filedialog.askdirectory(title = "Directory of folder",
                                            initialdir=outputtk.get())

            outputtk.insert(tk.END,files)


def p_pyinstall_and_dev(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
    except Exception:
            base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def removeexfilename(filename):
    """
    remove extension from file name
    EX:mmm.csv -----> mmm
    """
    return os.path.splitext(filename)[0]


def dirfolder (dirNamec, subforder,alertexists = True):
    """ create dir folder """
    try:
        dirName = os.makedirs(os.path.join(dirNamec, subforder))
    except:
        if alertexists:
            messagebox.showerror ("Error","{} already exists".format(subforder))
        else:
            pass
    return os.path.join(dirNamec, 
                        subforder)

def file_open(outputtk):
    """ ask directory file """
    outputtk.delete(0, 'end')    
    files = filedialog.askopenfilename(title = "Directory of parent file",
                                        initialdir=outputtk.get())

    outputtk.insert(tk.END,files)

def ask_directory(outputtk):
    """ ask directory """
    outputtk.delete(0, 'end')    
    folder = filedialog.askdirectory(title = "Directory of folder",
                                            initialdir=outputtk.get())
                                            
    outputtk.insert(tk.END,folder)


def ask_open(outputtk, 
                open_file = True):
        """ open directory file or folder"""
        outputtk.delete(0, 'end')
        file_open(outputtk) if open_file else ask_directory(outputtk)