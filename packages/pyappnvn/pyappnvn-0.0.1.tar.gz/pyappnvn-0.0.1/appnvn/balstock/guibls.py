import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pynvn.csv.rcsv import rcsv
from pynvn.csv.tocsv import wrcsv
from pathlib import Path

from pynvn.path.ppath import (getpathfromtk,
                                PathSteel,
                                ExtractFileNameFromPath,
                                PathFromFileNameAndDirpath,
                                abspath,
                                getdirpath,
                                ExtractFileNameFromPath,
                                getfilenamewoexten,
                                credirfol)
from pynvn.data.filename import namefile
from tkinter import messagebox
from datetime import datetime
from appnvn.balstock.dataexc import comparetwofile
import pandas as pd

def getdirpathfromorigin(output1):
        # Get path full 
        global pathinout
        pathinout = getpathfromtk(output1)
        filename =ExtractFileNameFromPath(pathinout)
        filename1 = getfilenamewoexten(filename)
        # get dirpath from full path
        dn = getdirpath(pathinout)

        ps = PathSteel(dir_path =dn,FileName = filename1 + ".csv")
        pathf = ps.refpath()
        return  pathf

class bl (tk.Tk):
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #self.setcfbs()
        nmgui(tktk = self).setcfbs()
        self.container = tk.Frame(self)
        #container.config(anchor=CENTER)
        self.container.pack(side="top",                           
                        fill=Y, expand=YES)  

        nmgui(tktk = self).createmenu()

        frame = nameuser(self.container, self)
        #self.frames[F] = frame
        frame.grid(row=0, 
                    column=0, 
                    sticky="nsew")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    

class nmgui:
    def __init__(self,tktk = None):
    # set logo and title 
        self.tktk = tktk
    def setcfbs (self):
        #self.tktk.iconbitmap('clienticon.ico')
        self.tktk.title (
                    "ATAD STEEL STRUCTURE CORPORATION"
                    )
        self.tktk.configure(background='khaki1')

    def createmenu (self):
        menubar = Menu(self.tktk)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", 
                            command=lambda: self.donothing())
        filemenu.add_command(label="Open", 
                            command=lambda: self.donothing())                                                                                                                   
        filemenu.add_command(label="Save", 
                            command=lambda: self.donothing())
        filemenu.add_command(label="Backup", 
                            command=lambda: self.donothing())
        filemenu.add_command(label="Close", 
                            command=lambda: self.donothing())

        filemenu.add_separator()

        filemenu.add_command(label="Exit", 
                            command=self.tktk.quit)
        menubar.add_cascade(label="Option", 
                            menu=filemenu)

        self.tktk.config(menu=menubar)

    def donothing(self):
        filewin = Toplevel(self.tktk)

        columns = ("#1","#2")

        self.tktk.tree = ttk.Treeview(filewin,
                                show = "headings",
                                columns = columns)

        self.tktk.tree.heading("#1", text="Name User")
        self.tktk.tree.heading("#2", text="Time")

        ysb = ttk.Scrollbar(filewin, orient=tk.VERTICAL,
        command=self.tktk.tree.yview)

        self.tktk.tree.configure(yscroll=ysb.set)

        pathf = getdirpathfromorigin(output1)
     
        dtpd = pd.read_csv(pathf,usecols=[0, 1], 
                                header=None)

        sh = dtpd.shape
        
        for ix in range(sh[0]):
            k = dtpd.iloc[ix] 
            k1 = k.values.tolist()
            self.tktk.tree.insert("", tk.END, 
                            values=k1)

        self.tktk.tree.grid(row=0, 
                    column=0)

        ysb.grid(row=0, 
                column=1, 
                sticky=tk.N + tk.S)

        self.tktk.rowconfigure(0, weight=1)
        self.tktk.columnconfigure(0, weight=1)
        button = Button(filewin,command=lambda: self.dowloadfilexcelfromeven(fullnamekkk), text="DownLoad")
        button.grid(row = 1,
                    column = 0,
                    sticky = "we"
                    )

        self.tktk.tree.column("#1",anchor=tk.CENTER)
        self.tktk.tree.column("#2",anchor=tk.CENTER)
        self.tktk.tree.bind("<<TreeviewSelect>>", self.print_selection)

    def returndirpath(self,filename1):
        pathfulloutput = self.getfullnamefromoutput()
        #filename1 = self.getfilenamefromoutput()
        dbk = credirfol(getdirpath(pathfulloutput),
                                    filename1)
        
        return dbk
    
    # get file name 
    def getfilenamefromoutput(self):
        pathfulloutput = self.getfullnamefromoutput()

        filename1 = getfilenamewoexten(ExtractFileNameFromPath(pathfulloutput)) 

        return filename1 
    
    def getfullnamefromoutput(self):

        pathfulloutput = getpathfromtk(output1)
        return pathfulloutput

    def print_selection(self,event):
        for selection in self.tktk.tree.selection():
            item = self.tktk.tree.item(selection)
            last_name, first_name = item["values"][0:2]
            #A = (last_name + first_name)
            namefilefromtkk = first_name.translate({ord(c): None for c in '!@#$?/: '}) + "_" + last_name
            namefilefromtkk1 = namefilefromtkk.replace(" ", "")

            dbk = self.returndirpath(self.getfilenamefromoutput())

            nf = namefile (dirpath = dbk,fnamesub = namefilefromtkk1)
            nflist = nf.returnfilfullnamefromsubname()
            global fullnamekkk
            fullnamekkk = PathFromFileNameAndDirpath(dir_path = dbk,
                                                filename = nflist)

    def dowloadfilexcelfromeven(self,fullname):
            # save as file path from path original 
            pathst = PathSteel (pathorigrn = fullname)
            pathst.saveasfiletopathAndopen()
            
class nameuser(tk.Frame):
    def __init__(self,parent, 
                controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self,
                        parent)

        self.inyname = Label(self,
                            text = "INPUT YOUR NAME",
                            width = 17, 
                            bg = "SteelBlue2",
                            fg="black"
                           )

        # create full path 
        self.pathcre = r"C:\NLT" 
        Path(self.pathcre).mkdir(parents=True,
                            exist_ok=True)
        # return path full 
        ps = PathSteel(dir_path =self.pathcre,
                    FileName = "nhuan.csv")    
        self.pathf = ps.refpath()
        rinput = rcsv(pathtor = self.pathf,indexarrtoget = [0])
        row = rinput.Rerowbyindxaindexarr()
        row = list(set(row))
        self.inynamein = ttk.Combobox(self, 
                                    values=row)

        self.button = tk.Button(self, text="Next",
                            command=lambda: self.checkinputyourname())
        self.inyname.pack()
        self.inynamein.pack()
        self.button.pack()

    def checkinputyourname(self):
        global inynameing
        inynameing = self.inynamein.get()
        if inynameing is "":
            print ("Check your name input:")
        else:
            global dt_string
            global dt_string_sr
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S %d/%m/%Y")
            dt_string_sr = now.strftime("%H%M%S%d%m%Y")
            self.controller.withdraw()
            filewin = Toplevel(self)
            app = primaryc(filewin)
            wv = wrcsv(pathtow = self.pathf,list =[inynameing])
            wv.writefilecsvFromRowArr()
            
class primaryc(bl):
    def __init__(self,master):
        self.master = master
        self.container = tk.Frame(self.master)
        self.container.pack()
        nmgui(tktk = master).createmenu()
        #bl.createmenu(self.master)
        large_font = ('Verdana',10)
        #bl.__init__ (self)
        nmgui(tktk = master).setcfbs()
        #create buttom for open file 
        button = tk.Button(self.container,text = "Directory file 1",
                            width = 10,
                            height = 2,
                            command = self.mfileopen
                            )
        button.grid(row = 0,
                    column = 0,
                    sticky = "we"
                    )

        self.master.protocol('WM_DELETE_WINDOW', 
                            self.doSomething)
        # create output text, it is used to save directory 
        self.output1 = tk.Text (self.container, 
                                width = 60,
                                height = 2,
                                font = large_font,
                                selectborderwidth = 10,
                                bg = "yellow"
                              )
        
        self.output1.grid(row = 0,
                        column = 1,
                        )
        global output1 
        output1 = self.output1
        
        # open file 1 
        self.openfile = tk.Button(self.container,text = "OPEN FILE 1",
                            width = 10,
                            height = 2,
                            command = lambda: self.openfile1(self.output1)
                            )

        self.openfile.grid(row = 0,
                    column = 2,
                    sticky = "we"
                    )

        # syn on server 
        self.syn = tk.Button(self.container,text = "SYN",
                            width = 5,
                            height = 2,
                            command = lambda: self.synserverfileexc(self.pathinout)
                            )
        self.syn.grid(row = 0,
                    column = 3,
                    sticky = "we"
                    )    

        #quit widget  
        buttom_quit = tk.Button (self.container,
                                text = "Exit",
                                width = 20,
                                command = self.container.quit
                                )

        buttom_quit.grid(row = 3,
                        column = 1,
                        )

    # open file follow directory 
    def mfileopen(self):
            files = filedialog.askopenfilename()
            self.output1.insert(tk.END,
                                files)
            
    # open file out put 
    def mfileopenout(self):
            files = filedialog.askopenfilename()
            self.output2.insert(tk.END,
                                    files)
    # Open file 1
    def openfile1 (self,output):
        # get path full
        self.pathinout = getpathfromtk(output)
        # save as file path from path original 
        pathst = PathSteel (pathorigrn = self.pathinout)
        pathst.saveasfiletopathAndopen()

    def synserverfileexc (self,pathtemp,indexcol = None):
        filenametemp = ExtractFileNameFromPath(path = pathtemp)

        dirname = abspath("")
        fullname = PathFromFileNameAndDirpath(dir_path = dirname,
                                            filename = filenametemp)                     
        ########################################
        pathfulloutput = getpathfromtk(output1)
        filename =ExtractFileNameFromPath(pathfulloutput)
        dbk = nmgui(tktk = self.master).returndirpath(getfilenamewoexten(filename))
        ########################################
        #create diff forder for diff file 
        dirpathdiff = nmgui(tktk = self.master).returndirpath("diff_history")
        inynameing1 = inynameing.replace(" ", " ")
        pathdiff = PathFromFileNameAndDirpath(dir_path = dirpathdiff,
                                            filename = dt_string_sr +\
                                                 "_" + inynameing1 +\
                                                      "_" + filename)

        ps = PathSteel(dir_path =dbk,
                        FileName = dt_string_sr +\
                                "_" + inynameing1 +\
                                     "_" + filename)
        dbk_fullpath = ps.refpath()

        #get path to orginal location with file name diff

        comparetwofile1 = comparetwofile(path_OLD = pathtemp,
                                        path_NEW = fullname,
                                        index_col = None,
                                        usernamein = inynameing1,
                                        pathtcsvtosavedata = getdirpathfromorigin(output1),
                                        difpathtobk = dbk_fullpath,
                                        pathtorgindiff = pathdiff,
                                        dt = dt_string) 
        comparetwofile1.excel_diff()
        
    def doSomething(self):
        if messagebox.askyesno("Exit",
                                "Do you want to quit the application?"):
            self.master.quit()
app = bl()
app.mainloop()