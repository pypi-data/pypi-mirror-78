import tkinter as tk 
from appnvn.exazp.exazb import azbg
import os
import tkinter as tk
from PIL import ImageTk
from pynvn.path.ppath import (
                            refullpath,
                            resource_path_is_from_pyinstall_and_dev,
                            listfileinfolder
                            )
from appnvn import key_license

class appazb:
    """ license key of app"""
    def __init__ (self,root = None):
        self.root = root
        dirname = os.path.dirname(__file__)
        
        # ===================================

        self.imagelogopath = resource_path_is_from_pyinstall_and_dev(refullpath(dirpath=dirname,
                                                                                    folderchild="img", 
                                                                                    filename="logo.png"
                                                                                    ))    

        self.imagelogo = ImageTk.PhotoImage(file =self.imagelogopath)

        self.pathconfig = resource_path_is_from_pyinstall_and_dev(refullpath(dirpath=dirname,
                                                                                    folderchild="config", 
                                                                                    filename="hrdata_modified.csv"
                                                                                    ))        


        self.pathconfigexell = resource_path_is_from_pyinstall_and_dev(refullpath(dirpath=dirname,
                                                                                    folderchild="config", 
                                                                                    filename="conf_ex.xlsx"
                                                                                    ))

        # path to config of excel to copy 
        
        self.pathconfigexcelcopy = resource_path_is_from_pyinstall_and_dev(refullpath(dirpath=dirname,
                                                                                    folderchild="config", 
                                                                                    filename="config_hm.xlsx"
                                                                                    ))
        
        # for license key 
        self.pathtokey =resource_path_is_from_pyinstall_and_dev(refullpath(dirpath=dirname,
                                                                            filename= "key.key",
                                                                            folderchild="config")
                                                                            )
        self.pathtovaluecsv_key = resource_path_is_from_pyinstall_and_dev(refullpath(dirpath=dirname,
                                                                                    folderchild="config", 
                                                                                    filename="fn.csv")
                                                                                    )
        self.ser_key = resource_path_is_from_pyinstall_and_dev(refullpath(dirpath=dirname,
                                                                                    folderchild="config", 
                                                                                    filename="seri.key")
                                                                                    )
        self.valueser_key = resource_path_is_from_pyinstall_and_dev(refullpath(dirpath=dirname,
                                                                                    folderchild="config", 
                                                                                    filename="ser.csv")
                                                                                    )                       
        
        self.azb = azbg(root=self.root,
                        imagelogopath =self.imagelogopath,
                        pathconfig = self.pathconfig,
                        pathconfigexell = self.pathconfigexell,
                        imagelogo = self.imagelogo,
                        pathconfigexcelcopy = self.pathconfigexcelcopy,
                        )
        key_license(root=self.root,
                    pathtokey=self.pathtokey,
                    pathtovaluecsv_key=self.pathtovaluecsv_key,
                    ser_key=self.ser_key,
                    valueser_key=self.valueser_key,
                    classofoject=self.azb
                    )

root = tk.Tk ()
obj = appazb(root)
root.mainloop()