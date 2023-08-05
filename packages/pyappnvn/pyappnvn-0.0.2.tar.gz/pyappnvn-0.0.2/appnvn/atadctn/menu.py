
import tkinter as tk
from tkinter import ttk
from appnvn.atadctn.folder.inputdoc import infolder
from appnvn.atadctn.layout.mlayout import mlayout
class menu:
    """set menu for atad"""
    def __init__(self,tktk = None,
                    pathicon = None,
                    pathclayout = None):
    # set logo and title 
        self.__tktk = tktk
        self.__pathicon = pathicon
        self.__pathclayout = pathclayout
    def createmenu (self):
        # create option
        menubar = tk.Menu(self.__tktk)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Add Layout", 
                            command=lambda: infolder(tktk=self.__tktk,
                                                    pathicon=self.__pathicon,
                                                    pathclayout =self.__pathclayout))
        filemenu.add_command(label="Modify Layout", 
                            command=lambda: mlayout(tktk=self.__tktk,
                                                    pathclayout=self.__pathclayout))

        filemenu.add_command(label="Save", 
                            command=lambda: mlayout(tktk=self.__tktk))
        filemenu.add_command(label="Backup", 
                            command=lambda: self.donothing())
        filemenu.add_command(label="Close", 
                            command=lambda: self.donothing())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", 
                            command=self.__tktk.quit)
        menubar.add_cascade(label="File", 
                            menu=filemenu)
        # create edit 
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label = "Undo", command = lambda: self.donothing())

        editmenu.add_separator()

        editmenu.add_command(label = "Cut", command = lambda: self.donothing())
        editmenu.add_command(label = "Copy", command = lambda: self.donothing())
        editmenu.add_command(label = "Paste", command = lambda: self.donothing())
        editmenu.add_command(label = "Delete", command = lambda: self.donothing())
        editmenu.add_command(label = "Select All", command = lambda: self.donothing())

        menubar.add_cascade(label = "Edit", menu = editmenu)

        # menu setting
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label = "language", command = lambda: self.donothing())
        helpmenu.add_command(label = "About...", command = lambda: self.donothing())
        menubar.add_cascade(label = "configuration", menu = helpmenu)


        # menu help
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label = "Help Index", command = lambda: self.donothing())
        helpmenu.add_command(label = "About...", command = lambda: self.donothing())
        menubar.add_cascade(label = "Help", menu = helpmenu)

        self.__tktk.config(menu=menubar)
    