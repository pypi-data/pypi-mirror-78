from tkinter import *
import tkinter as tk
from appnvn.atadctn.icontt import gui
from appnvn.atadctn.menu import menu
from tkinter import ttk
from appnvn.atadctn.treectn import (createcroll,
                                    ScrolledCanvas,
                                    cvframe,
                                    treescrollbar
                                    )
from appnvn.atadctn.spsquotation import spreadsheetgui

class layoutgui(Frame):
    def __init__(self,tktk = None,
                br_image = None,
                pathico = None,
                br_image_path = None):

        Frame.__init__(self, tktk)
        self.tktk = tktk

        self.br_image_path  = br_image_path

        self.br_image = br_image

        self.pathico = pathico

        self.filewin = Toplevel(self.tktk)

        gui (tktk=self.filewin,
                    pathico=self.pathico,
                    width=1280,
                    height=1024,
                    widthx=300,
                    widthy=0,
                    resizable=[True,True]).setcfbs()
        # set menu 
        menu (tktk=self.filewin).createmenu()

        #gui for data 
        self.sc  = ScrolledCanvas(self.filewin)
        self.listframeindata = self.sc.framea
        self.listFramevp =  createcroll(listFrame=self.listframeindata,
                                        cavheight=850,
                                        cavwidth=473).createy1()
        self.creategui()

        #set frame image 
        self.listframefim = self.sc.framec
        self.listFramevp4 =createcroll(listFrame=self.listframefim,
                                        cavwidth=1355,
                                        cavheight=850,
                                        scrollbarr=False).createy1()
        self.addimage()

        self.canv = self.sc.returncavas()
        
        # add buttom next and previous
        self.buttomandnext()
        self.createbutton(crheight= 900)

    def buttomandnext (self):

        button1 = Button(self.canv, 
                        text = "<<", 
                        anchor = CENTER)
        button1.configure(width = 3, 
                            activebackground = "#33B5E5", 
                            relief = FLAT)
        button1_window = self.canv.create_window(1170, 900, 
                                                anchor=NW, 
                                                window=button1)
        button1 = Button(self.canv, 
                        text = ">>", 
                        anchor = CENTER)
        button1.configure(width = 3, 
                            activebackground = "#33B5E5", 
                            relief = FLAT)
        button1_window = self.canv.create_window(1210, 900, 
                                                anchor=NW, 
                                                window=button1)      

    def addimage(self):
        price = tk.Label(self.listFramevp4,
                            image = self.br_image_path,
                            bd = 0
                        )
        price.pack(fill=BOTH ,
                    expand=YES)
                    
    def creategui(self):      
        add = tk.Label(self.listFramevp,text = "Add:",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 0,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        #input price
        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "Zamboanga, Philippines"
                            )
        add.grid(column = 1, 
                        row  = 0 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "w",
                        )

        #  ITEM

        add = tk.Label(self.listFramevp,text = "TEM:",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 1,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "PRE-ENGINEERED STEEL BUILDING"
                            )
        add.grid(column = 1, 
                        row  = 1 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "w",
                        )
        # date
        
        add = tk.Label(self.listFramevp,text = "Date:",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 2,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            anchor="center",
                            width = 37,
                            text = "08/04/2020"
                            )
        add.grid(column = 1, 
                        row  = 2 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "e",
                        )

        #   BOQ type
        
        add = tk.Label(self.listFramevp,text = "BOQ type:",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 3,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "Lump sum"
                            )
        add.grid(column = 1, 
                        row  = 3 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "e",
                        )

        #   BOQ type
        
        add = tk.Label(self.listFramevp,text = "Contact person:",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 4,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "LRenante Bendana"
                            )
        add.grid(column = 1, 
                        row  = 4 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "e",
                        )

        # Phone
        
        add = tk.Label(self.listFramevp,text = "Contact person:",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 5,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "+63 966 483 5871"
                            )
        add.grid(column = 1, 
                        row  = 5 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "e",
                        )


        #   Office
        
        add = tk.Label(self.listFramevp,text = "Office:",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 6,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "99 Nguyen Thi Minh Khai, Ben Thanh W, Dist 1, HCMC"
                            )
        add.grid(column = 1, 
                        row  = 6 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "e",
                        )

        #   CHECKCHECK
        
        add = tk.Label(self.listFramevp,text = "CHECK:",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 7,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "TTT"
                            )
        add.grid(column = 1, 
                        row  = 7 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "e",
                        )
        # DONE
        
        add = tk.Label(self.listFramevp,text = "DONE:",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 8,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "LAHP"
                            )
        add.grid(column = 1, 
                        row  = 8 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "e",
                        )

        #   BOQ expired date
        
        add = tk.Label(self.listFramevp,text = "BOQ expired date:",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 9,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "within 30 days"
                            )
        add.grid(column = 1, 
                        row  = 9 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "e",
                        )

        #  QUANTITY CONTAINER
        
        add = tk.Label(self.listFramevp,text = "Quantity Container",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 10,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "3"
                            )
        add.grid(column = 1, 
                        row  = 10 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "e",
                        )

        #  QUANTITY Toilet
        
        add = tk.Label(self.listFramevp,text = "Quantity Toilet",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 11,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "3"
                            )
        add.grid(column = 1, 
                        row  = 11 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "e",
                        )
    
        #  QUANTITY Toilet
        
        add = tk.Label(self.listFramevp,text = "Quantity bedroom",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 12,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "3"
                            )
        add.grid(column = 1, 
                        row  = 12 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "e",
                        )

        #  sample 1
        
        add = tk.Label(self.listFramevp,text = "Sample 1",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 13,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "3"
                            )
        add.grid(column = 1, 
                        row  = 13 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "e",
                        )

        # sample 2 
        add = tk.Label(self.listFramevp,text = "Sample 2",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 14,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "3"
                            )
        add.grid(column = 1, 
                        row  = 14 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "e",
                        )
        #sample 3
        add = tk.Label(self.listFramevp,text = "Sample 3",
                            anchor="center",
                            width = 15,
                            height = 1,
                            )
        add.grid(column = 0, 
                  row = 15,
                  pady = 20, 
                  padx = (50,0),
                  sticky  = W)

        add = tk.Label(self.listFramevp,
                            width = 37,
                            anchor="center",
                            text = "3"
                            )
        add.grid(column = 1, 
                        row  = 15 ,
                        pady = 20,
                        padx = 1,
                        sticky  = "e",
                        )
    

    def createbutton (self,crwidth = 180 ,crheight = 480,namebutton ="QUOTATION DETAIL",width = 15):
    
      button1 = Button(self.canv, 
                      text = namebutton,
                      command = lambda: spreadsheetgui(tktk=self.tktk,
                                                        pathico=self.pathico,
                                                        br_image_path=self.br_image_path),
                      anchor = CENTER)
      button1.configure(width = width, 
                        activebackground = "#33B5E5", 
                        relief = FLAT),
      button1_window = self.canv.create_window(crwidth, crheight, 
                                              anchor=NW, 
                                              window=button1)
    
