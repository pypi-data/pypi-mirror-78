import tkinter as tk # python 3
from appnvn.atadctn.treectn import scbg
from appnvn.atadctn.icontt import gui
from tkinter import filedialog
from pynvn.path.ppath import credirfol,listfileinfolder,getpathfromtk
from pynvn.list.flist import filterlistbylstr
import shutil
class infolder(tk.Tk):
    """ config layout, add layout more from input user """
    def __init__(self, 
                    tktk = None,
                    pathicon =None,
                    *args,
                    labelfont = ('times', 20),
                    labelfont_sm = ('times', 16),
                    labelfont_botton = ('times', 11), 
                    pathclayout = None,
                    namequotation = "quotation.xlsx",
                    **kwargs):
       
        self.__tktk = tktk
        self.__labelfont = labelfont
        self.__labelfont_sm = labelfont_sm
        self.__pathclayout = pathclayout
        self.__labelfont_botton = labelfont_botton
        self.__filewin = tk.Toplevel(self.__tktk)
        self.__namequotation = namequotation
        gui (tktk=self.__filewin,
            pathico=pathicon,
            width=800,
            height=800,
            widthx="center",
            widthy="center",
            resizable=[True,True],
            condv=2.7
            )\
            .setcfbs()
        container = tk.Frame(self.__filewin,
                            bg = "white")
        container.pack(side="top",
                        fill="both", 
                        expand=True)

        #gui for data 
        self.__sc = scbg(parent = container,
                        cavheight=600,
                        cavwidth=600,
                        bg = "white", 
                        bgpr = "#5b9bd5"
                        )

        self.__listFramevp = self.__sc.framecv
        self.__creategui()
    def __creategui(self):
        """ create to input size layout """
        row = 0
        sltt = tk.Label(self.__listFramevp,
                        text = "Input your layout infomation",
                        font=self.__labelfont,
                        bg = "white",
                        )
        sltt.grid(column = 1, 
                        row = row,
                        pady = 10,
                        sticky  = tk.W)

        row = row + 1
        sl = tk.Label(self.__listFramevp,
                        text = "*Size Layout:",
                        bg = "white",
                        font=self.__labelfont_sm
                        )
        sl.grid(column = 0, 
                        row = row,
                        pady = 10,
                        sticky  = tk.W)

        self.vsle = tk.IntVar(self.__listFramevp, 
                            value=6000
                            )
            
        sle = tk.Entry(self.__listFramevp,
                        justify=tk.CENTER,
                        textvariable = self.vsle,
                        font=self.__labelfont_sm,
                        bg = "white",
                        relief = tk.SOLID
                        )
        sle.grid(column = 1, 
                        row  = row,
                        pady = 10,
                        sticky  = tk.EW,
                        )
        #width of layout 
        slw = tk.Label(self.__listFramevp,
                        text = "*Width",
                        bg = "white",
                        font=self.__labelfont_sm
                        )
        slw.grid(column = 2, 
                        row = row,
                        pady = 10,
                        sticky  = tk.W)

        #Height of layout
        row = row + 1
        self.vslh = tk.IntVar(self.__listFramevp, 
                            value=6000
                            )

        slh = tk.Entry(self.__listFramevp,
                        justify=tk.CENTER,
                        textvariable = self.vslh,
                        bg = "white",
                        font=self.__labelfont_sm,
                        relief = tk.SOLID
                        )

        slh.grid(column = 1, 
                        row  = row,
                        pady = 10,
                        sticky  = tk.EW,
                        )

        slw = tk.Label(self.__listFramevp,
                        text = "*Height",
                        font=self.__labelfont_sm,
                        bg = "white",
                        )
        slw.grid(column = 2, 
                        row = row,
                        pady = 10,
                        sticky  = tk.W)        
    
        #note of layout
        row = row + 1
        self.vsln = tk.StringVar(self.__listFramevp, 
                            value="Note"
                            )

        sln = tk.Entry(self.__listFramevp,
                        textvariable = self.vsln,
                        justify=tk.CENTER,
                        bg = "white",
                        font=self.__labelfont_sm,
                        relief = tk.SOLID
                        )

        sln.grid(column = 1, 
                        row  = row,
                        pady = 10,
                        sticky  = tk.EW,
                        )

        note = tk.Label(self.__listFramevp,
                        text = "*Note",
                        font=self.__labelfont_sm,
                        bg = "white",
                        )
        note.grid(column = 2, 
                        row = row,
                        pady = 10,
                        sticky  = tk.W)
        
        # path to folder image 
        row = row + 1
        pdi = tk.Label(self.__listFramevp,
                        text = "*Path to image folder:",
                        font=self.__labelfont_sm,
                        bg = "white",
                        
                        )
        pdi.grid(column = 0, 
                row = row,
                pady = 10,
                sticky  = tk.W)

        # create output text, it is used to save directory 
        self.output1 = tk.Entry (self.__listFramevp, 
                                justify=tk.CENTER,
                                relief = tk.SOLID,
                                font=self.__labelfont_sm,
                                bg = "white"
                              )
        self.output1.grid(row = row,
                        column = 1,
                        pady = 10,
                        sticky  = tk.EW
                        )
        button1 = tk.Button(self.__listFramevp,
                            font=self.__labelfont_botton,
                            bd = 1,
                            command = lambda: self.askfolderlayout()
                            )
        button1.grid(row = row,
                    column = 2,
                    pady = 10,
                    sticky = "we"
                    )

        # path to folder image 
        row = row + 1
        pdi = tk.Label(self.__listFramevp,
                        text = "*Path to quotation:",
                        font=self.__labelfont_sm,
                        bg = "white",
                        )
        pdi.grid(column = 0, 
                        row = row,
                        pady = 10,
                        sticky  = tk.W)

        # create output text, it is used to save directory 
        self.output2 = tk.Entry (self.__listFramevp, 
                                justify=tk.CENTER,
                                relief = tk.SOLID,
                                font=self.__labelfont_sm,
                                bg = "white"
                              )
        self.output2.grid(row = row,
                        column = 1,
                        pady = 10,
                        sticky  = tk.EW,
                        )
        button2 = tk.Button(self.__listFramevp,
                            font=self.__labelfont_botton,
                            bd = 1,
                            command = lambda: self.mfileoquation()
                            )
        button2.grid(row = row,
                    column = 2,
                    pady = 10,
                    sticky = "we"
                    )
        # update data
        button = tk.Button(self.__listFramevp,
                            height = 1,
                            text = "Update Data",
                            width = 4,
                            command = lambda: self.tranferdatatofolder(),
                            bd = 1,
                            )
        row = row + 1
        button.grid(row = row,
                    column = 1,
                    pady = 10,
                    sticky = "we"
                    )
        # exit 
        buttone = tk.Button(self.__listFramevp,
                            height = 1,
                            text = "Exit",
                            width = 4,
                            command =lambda: self.__filewin.withdraw(),
                            bd = 1,
                            )
        row = row + 1 
        buttone.grid(row = row,
                    column = 1,
                    pady = 10,
                    sticky = "we"
                    )

    def askfolderlayout(self):
        self.output1.delete(0, 'end')
        # ask directory
        files = filedialog.askdirectory(title = "Directory of child files",
                                        initialdir=self.output1.get())
        self.output1.insert(tk.END,files)

    def mfileoquation(self):
        """ open file parent"""
        self.output2.delete(0, 'end')
        # ask directory
        files = filedialog.askopenfilename(title = "Directory of parent file",
                                            initialdir=self.output2.get())
        self.output2.insert(tk.END,
                            files)
    def __createfoldername(self):
        """ return name """
        return str(self.vsle.get())+ "x" + str(self.vslh.get()) + "_"  + self.vsln.get()
    def __createfolderbyname(self):
        """ create folder of layout stock quotation and image"""
        return credirfol(dirNamec = self.__pathclayout,
                subforder=self.__createfoldername())
        
    def returnlistfileinfolder(self):
        """ return list file in folder"""
        pathtocopy = getpathfromtk(self.output1)
        lfilecopy = listfileinfolder(pathtocopy)
        lfileafterfilter = filterlistbylstr (criteria=[".gif",".jpg"],
                                            liststr=lfilecopy)
        return lfileafterfilter
    
    def tranferdatatofolder (self):
        """tranfer data to folder"""
        # copy file image layout 
        pathcopy = self.__createfolderbyname()
        for f in self.returnlistfileinfolder():
            shutil.copy(f,pathcopy)
        # copy file excel quotation 
        fileexqu = self.returnfiletocopyquotation()
        shutil.copy(fileexqu,
                    pathcopy + "/" + self.__namequotation)

    def returnfiletocopyquotation(self):
        """ return path file excel in folder """
        return getpathfromtk(self.output2)