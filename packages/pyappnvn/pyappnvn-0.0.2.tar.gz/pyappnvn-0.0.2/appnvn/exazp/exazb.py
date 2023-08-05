from tkinter import Button, Frame,messagebox
import os
from appnvn.atadctn.icontt import gui
import tkinter as tk
from tkinter import filedialog
from pynvn.path.ppath import getpathfromtk
from appnvn.atadctn.treectn import scbg
from pathlib import Path
from PIL import ImageTk
from pynvn.path.ppath import (refullpath,
                            listfileinfolder
                            )
from appnvn.atadctn.treectn import scrollbarvn
from pynvn.checklb.checkb import ChecklistBox
from pynvn.excel.copyexcel import cexcel
from pynvn.excel.hexcel import hexcel_child
from pynvn.excel.lexcel import listexcel
from appnvn.exazp.excel import hexcel
from pynvn.list.flist import filterlistbylstr
from appnvn.exazp.sdata.sdata import covertcsvexcel
from appnvn.exazp.excel.crangeactive import crangeactive
from appnvn.exazp.excel.hhm import hdatahm
from pynvn.excel import openexcelbyxl
from appnvn.exazp.conf import hconfazb
from pynvn.excel import closeallfileexcel
class azbg:
    """ return azbg gui """
    def __init__ (self,
                root=None,
                imagelogopath =None,
                pathconfig = None,
                pathconfigexell = None,
                imagelogo = None,
                pathconfigexcelcopy = None
                ):

        self.root = root 
        self.imagelogopath =imagelogopath
        self.pathconfig = pathconfig
        self.pathconfigexell = pathconfigexell
        self.imagelogo = imagelogo
        self.pathconfigexcelcopy =pathconfigexcelcopy
    def guiforgd(self):
        gui (tktk=self.root,
            pathico=None,
            width=700,
            height=700, 
            widthx=420, 
            widthy=0,
            resizable=[True,True],
            title= "AZB").setcfbs()

        self.sc  = scbg(parent = self.root,
                        cavheight=420,
                        cavwidth=470,
                        isonlyaframe= False,
                        bg = "#e6ecf5",
                        bgpr = "#5b9bd5",
                        framea = [0,0,470,130,"#e6ecf5"],
                        frameb = [0,130,470,100,"white"],
                        framec = [0,240,470,160,"#e6ecf5"],
                        )
        large_font = ("times new roman",12)
        lb = tk.Label(self.root,
                    text = "Creator: Mr.Hoàng + Mr.Đồng",
                    font = large_font,bg ="#5b9bd5")
        lb.place(relx = 0.5, 
                rely = 0.87, 
                anchor = tk.CENTER
                )
        lb = tk.Label(self.root,
                    text = "Programmer: Mr. Nhuần - nhuannv.vs@gmail.com",
                    font = large_font,bg ="#5b9bd5" 
                    )

        lb.place(relx = 0.5, 
                    rely = 0.9, 
                    anchor = tk.CENTER)
            
        self.framea = self.sc.framea
        self.frameb = self.sc.frameb
        self.framec = self.sc.framec
        

        lbt = tk.Label (self.framea, 
                        bg = "#e6ecf5" ,
                        image = self.imagelogo,
                        
                        )
        lbt.grid(row = 0,
                    column = 0,
                    columnspan = 3,
                    sticky = tk.EW
                    )
        # path to folder child
        lbt1 = tk.Label(self.framea,
                        text = "Path To Folder:", 
                        width = 10,
                        font =large_font,
                        bg = "#e6ecf5",)
        lbt1.grid(row = 1,
                    column = 0,
                    sticky =  tk.W
                    )
        # create output text, it is used to save directory 
        self.output1 = tk.Entry (self.framea, 
                                font = large_font,
                                justify=tk.CENTER,
                                width = 40,
                                relief = tk.SOLID,
                                bg = "yellow"
                              )
        self.output1.grid(row = 1,
                        column = 1,
                        )
        button = tk.Button(self.framea,
                            height = 1,
                            width = 4,
                            bd = 1,
                            command = lambda: self.mfolderopenchild()
                            )
        button.grid(row = 1,
                    column = 2,
                    sticky = "we"
                    )

        # path to folder parent file 
        lbt1 = tk.Label(self.framec,
                        text = "Path To Pfile:", 
                        width = 10,
                        font =large_font,
                        bg = "#e6ecf5")
        lbt1.grid(row = 0,
                    column = 0,
                    sticky = tk.W
                    )
        # frame c 
        # create output text, it is used to save directory 
        self.output1p = tk.Entry (self.framec, 
                                font = large_font,
                                justify=tk.CENTER,
                                width = 40,
                                relief = tk.SOLID,
                                bg = "yellow"
                              )

        self.output1p.grid(row = 0,
                        column = 1,
                        )
        button = tk.Button(self.framec,
                            height = 1,
                            width = 4,
                            bd = 1,
                            command = lambda: self.mfileopenparent()
                            )
        button.grid(row = 0,
                    column = 2,
                    sticky = "we"
                    )
        #copy past range
        self.openfile5 = tk.Button(self.framec,text = "Copy HM",
                            width = 10,
                            height = 1,
                            command = lambda: crangeactive(pathconf=self.pathconfig,
                                                            pathconfigexcelcopy=self.pathconfigexcelcopy).copyrangfromconf()
                            )
        self.openfile5.grid(row = 1, column = 1,sticky = "w")
        
        #copy past range
        self.openfile5 = tk.Button(self.framec,text = "Fct",
                            width = 10,
                            height = 1,
                            command = lambda: hdatahm(pathconf=self.pathconfig)
                            )
        self.openfile5.grid(row = 1, column = 1,sticky = "e")

        #only handling data tong hop
        self.openfile2 = tk.Button(self.framec,text = "ValueFTHVT",
                            width = 10,
                            height = 1,
                            command =  lambda: hexcel(pathconf =  self.pathconfig).valuehangmucforthvt()
                            )
        self.openfile2.grid(row = 2, column = 1,sticky = "w")

        #only handling to parent
        self.openfile4 = tk.Button(self.framec,text = "Update Data",
                            width = 10,
                            height = 1,
                            command = lambda: hexcel(pathconf =  self.pathconfig,
                                                    pathconfigexcelcopy=self.pathconfigexcelcopy).gdatafromothersheet()
                            )

        self.openfile4.grid(row = 2, column = 1,sticky = "e")

        #only handling data kid
        self.openfile1 = tk.Button(self.framec,text = "Child",
                            width = 10,
                            height = 1,
                            command = lambda: self.hdatafilechecked()
                            )

        self.openfile1.grid(row = 3, column = 1,sticky = "w")

        #only handling to parent
        self.openfile3 = tk.Button(self.framec,text = "Run To Parent",
                            width = 10,
                            height = 1,
                            command = lambda: self.getCheckedItem()
                            )

        self.openfile3.grid(row = 3, column = 1,sticky = "e")

        # open conf excel
        self.openfile3a = tk.Button(self.framec,text = "open config",
                            width = 10,
                            height = 1,
                            command = lambda: openexcelbyxl(self.pathconfigexell)
                            )
        self.openfile3a.grid(row = 4, column = 1,sticky = "w")

        # open conf excel
        self.openfile3b = tk.Button(self.framec,text = "update config",
                            width = 10,
                            height = 1,
                            command = lambda: hconfazb(pathconf=self.pathconfig,
                                                    pathexconf=self.pathconfigexell).convertocsv()
                            )
        self.openfile3b.grid(row = 4, column = 1,sticky = "e")

        # open conf excel
        self.openfile3a = tk.Button(self.framec,text = "Temp excelhm",
                            width = 10,
                            height = 1,
                            command = lambda: openexcelbyxl(self.pathconfigexcelcopy)
                            )
        self.openfile3a.grid(row = 5, column = 1,sticky = "w")

        #only handling to parent
        self.openfile5 = tk.Button(self.framec,text = "Update PTVT",
                            width = 10,
                            height = 1,
                            command = lambda: covertcsvexcel(pathconf=self.pathconfig)
                            )
        self.openfile5.grid(row = 5, column = 1,sticky = "e")
        #item identification
          
        buttom_quit = tk.Button (self.framec,
                                text = "Item iden",
                                width = 10,
                                height = 1,
                                command = lambda: self.itemiden()
                                )
        buttom_quit.grid(row = 2, column = 1)

        #quit widget
        buttom_quit = tk.Button (self.framec,
                                text = "Exit",
                                width = 10,
                                height = 1,
                                command = self.root.quit
                                )
        buttom_quit.grid(row = 3, column = 1)    
    # open file follow directory 
    def mfolderopenchild(self):
        """ open folder of child files"""
        try: 
            closeallfileexcel(namek_ofpname="AZB")
        except:
            pass
        self.output1.delete(0, 'end')
        # ask directory
        files = filedialog.askdirectory(title = "Directory of child files",
                                        initialdir=self.output1.get())
        self.output1.insert(tk.END,files)
        # get path from entry 
        self.pathin = getpathfromtk(self.output1)
        try: 
            self.scf.destroy()
        except:
            pass
        self.scf = scrollbarvn(parent=self.frameb,
                                bg = "white")
        self.scframe = self.scf.frame
        if self.pathin:
            # return list in folder 
            fpexcel = listfileinfolder(self.pathin) 
            # filter file in folder 
            plist = filterlistbylstr (criteria=["AZB"],liststr=fpexcel)

            # return list path excel sheeet
            lpsheet = [refullpath(dirpath=self.pathin,
                                filename = fpname) for fpname in plist]
            
            # return list sheet excel
            lsexcel = listexcel(l_ex=lpsheet).returnlsheet()
            # create check list box 
            self.cb = ChecklistBox(parent=self.scframe,
                        choices=plist,
                        listsheetname=lsexcel,
                        width= 123)

    def mfileopenparent(self):
        """ open file parent"""
        self.output1p.delete(0, 'end')
        # ask directory
        files = filedialog.askopenfilename(title = "Directory of parent file",
                                            initialdir=self.output1p.get())
        self.output1p.insert(tk.END,
                            files)
        # get path from entry 
        self.pathfilep = getpathfromtk(self.output1p)
    def getCheckedItem(self):
        """ get checked item """
        listcheked =  self.cb.getCheckedItems()
        for eleexcell in listcheked:
            pathtocopy = refullpath(dirpath=self.pathin,
                                    filename = eleexcell)     
            cexcel(pathdes=self.pathfilep,
                    pathtocopy=pathtocopy,
                    pathconf=self.pathconfig).copysheettoexcelexist()
    def hdatafilechecked(self):
        """halding data value"""
        try:
            listcheked =  self.cb.getCheckedItems()
        except:
            messagebox.showerror ("Error list file", "Check path to child, no file checked")
        for eleexcell in listcheked:
            pathtocopy = refullpath(dirpath=self.pathin,
                                    filename = eleexcell)
            hexcel_child(pathtocopy=pathtocopy,
                        pathconf = self.pathconfig,
                        diplaywindow = self.root).runaz30azb60()  
    def itemiden(self):
        try:
            listcheked =  self.cb.getCheckedItems()
        except:
            messagebox.showerror ("Error list file", "Check path to child, no file checked")
        for eleexcell in listcheked:
            pathtocopy = refullpath(dirpath=self.pathin,
                                    filename = eleexcell)
            hexcel_child(pathtocopy=pathtocopy,
                        pathconf = self.pathconfig,
                        diplaywindow = self.root).runaz30azb60(onlyitemiden= True)  
