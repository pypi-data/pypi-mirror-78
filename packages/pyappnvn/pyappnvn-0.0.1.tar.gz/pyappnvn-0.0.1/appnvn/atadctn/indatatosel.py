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
class indatagui(Frame):
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

        #gui for inputdata 
        self.sc  = ScrolledCanvas(self.filewin)
        self.listframeindata = self.sc.framea
        self.listFramevp =  createcroll(listFrame=self.listframeindata,
                                        cavheight=450,
                                        cavwidth=473).createy1()

        # gui for resurlt
        self.listframert =self.sc.frameb
        self.listFramevp2 = createcroll(listFrame=self.listframert,
                                        cavwidth=490,
                                        cavheight=442,
                                        scrollbarr=False).createy1()
        self.seleevent()


        #set frame image 
        self.listframefim = self.sc.framec
        self.listFramevp4 =createcroll(listFrame=self.listframefim,
                                        cavwidth=1355,
                                        cavheight=455,
                                        scrollbarr=True).createy1()
        self.addimage()

        # add quotation 
        self.framequation = self.sc.framed
        
        self.framequationin =createcroll(listFrame=self.framequation,
                                        cavwidth=1355,
                                        cavheight=440,
                                        scrollbarr=False).createy1()
        
        self.quotationforctn()
        
        self.canv = self.sc.returncavas()

        # add buttom next and previous
        self.buttomandnext()

        #create buttom "Next"
        self.createbutton()
        #create buttom modify
        self.createbutton(crheight= 530,crwidth= 580,namebutton= "VIEW FULL")

    def buttomandnext (self):

        button1 = Button(self.canv, 
                        text = "<<", 
                        anchor = CENTER)
        button1.configure(width = 3, 
                            activebackground = "#33B5E5", 
                            relief = FLAT)
        button1_window = self.canv.create_window(1170, 480, 
                                                anchor=NW, 
                                                window=button1)
        button1 = Button(self.canv, 
                        text = ">>", 
                        anchor = CENTER)
        button1.configure(width = 3, 
                            activebackground = "#33B5E5", 
                            relief = FLAT)
        button1_window = self.canv.create_window(1210, 480, 
                                                anchor=NW, 
                                                window=button1)      

    def addimage(self):
        price = tk.Label(self.listFramevp4,
                            image = self.br_image_path,
                            bd = 0
                        )
        price.pack(fill=BOTH ,expand=YES)

    def seleevent(self):
            columns = ("#1", "#2", "#3")
            self.tree = ttk.Treeview(self.listFramevp2, 
                                    show="headings",
                                    height = 20,
                                    columns=columns)
            self.tree.heading("#1", text="OPTION")
            self.tree.heading("#2", text="DESCRIPTION")
            self.tree.heading("#3", text="PRICE")
            treescrollbar(frame=self.listFramevp2,tree=self.tree).treescrollbar2r()
            self.tree.pack(expand=YES,fill=BOTH)

            self.tree.column("#1",
                            minwidth=0,
                            width=150, 
                            stretch=NO)
            self.tree.column("#2",
                            minwidth=0,
                            width=150, 
                            stretch=NO)

            self.tree.column("#3",
                            minwidth=0,
                            width=150, 
                            stretch=NO)
    
    # qotation for container 
    def quotationforctn(self):
            # frame to modify date, issue
            frame1 = Frame(self.framequationin) 
            frame1.pack(pady = (5,10)) 

            b1 = Label(frame1, text = "Project ID") 
            b1.grid (column = 0, row = 0)

            entryeditor = tk.Entry(frame1,
                            width = 15,
                            justify=CENTER
                            )
            entryeditor.grid (column = 1, row = 0)
            

            b1 = Label(frame1, text = "Project Name") 
            b1.grid (column = 2, row = 0,sticky = tk.W)

            entryeditor = tk.Entry(frame1,
                            width = 15,
                            justify=CENTER
                            )
            entryeditor.grid (column = 3, row = 00)


            b1 = Label(frame1, text = "Person editor") 
            b1.grid (column = 4, row = 0)

            entryeditor = tk.Entry(frame1,
                            width = 15,
                            justify=CENTER
                            )
            entryeditor.grid (column = 5, row = 0)

            
            b1 = Label(frame1, text = "Date Release") 
            b1.grid (column = 6, row = 0)

            entryeditor = tk.Entry(frame1,
                            width = 15,
                            justify=CENTER
                            )
            entryeditor.grid (column = 7, row = 0)

            columns = ("#1", "#2", "#3","#4", "#5", "#6","#7")
            self.tree = ttk.Treeview(self.framequationin,  
                                    height = 18,
                                    show="headings", 
                                    columns=columns)
            self.tree.heading("#1", text="NO.")
            self.tree.heading("#2", text="DESCRIPTION")
            self.tree.heading("#3", text="UNIT")
            self.tree.heading("#4", text="QUANTITY")
            self.tree.heading("#5", text="AMOUNT")
            self.tree.heading("#6", text="REMARK")
            self.tree.heading("#7", text="NOTE")

            treescrollbar(frame=self.framequationin,tree=self.tree).treescrollbar2r()

            self.tree.pack(expand=YES,fill=BOTH,side = BOTTOM)


            self.tree.column("#1",
                            minwidth=0,
                            width=50, 
                            stretch=NO)
            self.tree.column("#2",
                            minwidth=0,
                            width=300, 
                            stretch=NO)

            self.tree.column("#3",
                            minwidth=0,
                            width=50, 
                            stretch=NO)
            self.tree.column("#4",
                            minwidth=0,
                            width=300, 
                            stretch=NO)
            self.tree.column("#5",
                            minwidth=0,
                            width=300, 
                            stretch=NO)
            self.tree.column("#6",
                            minwidth=0,
                            width=300, 
                            stretch=NO)
            self.tree.column("#7",
                            minwidth=0,
                            width=300, 
                            stretch=NO)

    def createbutton (self,crwidth = 180 ,crheight = 480,namebutton ="FIND"):
    
      button1 = Button(self.canv, 
                      text = namebutton,
                      command = lambda: spreadsheetgui(tktk=self.tktk,
                                                        pathico=self.pathico,
                                                        br_image_path=self.br_image_path),
                      anchor = CENTER)
      button1.configure(width = 10, 
                        activebackground = "#33B5E5", 
                        relief = FLAT)
      button1_window = self.canv.create_window(crwidth, crheight, 
                                              anchor=NW, 
                                              window=button1)

    def creategui(self):      
        price = tk.Label(self.listFramevp,text = "Price you can pay ?",
                            width = 40,
                            height = 1,
                            )
        price.grid(column = 0, 
                  row = 0,
                  pady = 20,
                  padx = (25,0),
                  sticky  = W)

        #input price
        inputprice = tk.Entry(self.listFramevp,
                            width = 15,
                            )
        inputprice.grid(column = 1, 
                        row  = 0,
                        padx = (20,0),
                        pady = 20,
                        sticky  = E
                        )
        
        #area 
        area = tk.Label(self.listFramevp,text = "How much house area do you want ?",
                            width = 40,
                            height = 1,
                            )
        area.grid(column = 0, 
                  row = 1,
                  padx = (25,0),
                  sticky  = W,
                  pady = 20)
        #area m2
        aream = tk.Entry(self.listFramevp,
                            width = 15,
                            justify=CENTER
                            )
        aream.grid(column = 1, 
                  row = 1,
                  pady = 20,
                  padx = (20,0),
                  sticky  = E)

        #many room 
        area = tk.Label(self.listFramevp,text = "How many rooms do you want to house?",
                            width = 40,
                            height = 1,
                            )
        area.grid(column = 0, 
                  row = 2,
                  padx = (25,0),
                  sticky  = W,
                  pady = 20)

        #many room
        aream = tk.Entry(self.listFramevp,
                            width = 15,
                            justify=CENTER,
                            )
        aream.grid(column = 1, 
                    row = 2,
                    padx = (20,0),
                    sticky  = E,
                    pady = 20)

        #many toilet 
        area = tk.Label(self.listFramevp,text = "How many rooms do you want to toilet?",
                            width = 40,
                            height = 1,
                            )
        area.grid(column = 0, 
                  row = 3,
                  padx = (25,0),
                  sticky  = W,
                  pady = 20)

        #many toilet
        aream = tk.Entry(self.listFramevp,
                            width = 15,
                            justify=CENTER,
                            )
        aream.grid(column = 1, 
                  row = 3,
                  padx = (20,0),
                  sticky  = E,
                  pady = 20)


        ######### colum 0 and 1
        price = tk.Label(self.listFramevp,text = "Price you can pay ?",
                            width = 40,
                            height = 1,
                            )
        price.grid(column = 0, 
                    row = 4,
                    padx = (25,0),
                    sticky  = W)

        #input price
        inputprice = tk.Entry(self.listFramevp,
                            width = 15,
                            justify=CENTER,
                            )
        inputprice.grid(column = 1, 
                        row  = 4 ,
                         padx = (20,0),
                        pady = 20,
                        sticky  = E
                        )
        
        #area 
        area = tk.Label(self.listFramevp,text = "How much house area do you want ?",
                            width = 40,
                            height = 1,
                            )
        area.grid(column = 0, 
                  row = 5,
                  padx = (25,0),
                  sticky  = W,
                  pady = 20)

        #area m2
        aream = tk.Entry(self.listFramevp,
                            width = 15,
                            justify=CENTER
                            )
        aream.grid(column = 1, 
                  row = 5,
                  padx = (20,0),
                  pady = 20,
                  sticky  = E)

        #many room 
        area = tk.Label(self.listFramevp,text = "How many rooms do you want to house?",
                            width = 40,
                            height = 1,
                            )
        area.grid(column = 0, 
                row = 6,
                padx = (25,0),
                sticky  = W,
                pady = 20)

        #many room
        aream = tk.Entry(self.listFramevp,
                            width = 15,
                            justify=CENTER,
                            )
        aream.grid(column = 1, 
                  row = 6,
                  padx = (20,0),
                  sticky  = E,
                  pady = 20)

        #many toilet 
        area = tk.Label(self.listFramevp,text = "How many rooms do you want to toilet?",
                            width = 40,
                            height = 1,
                            )
        area.grid(column = 0, 
                  row = 7,
                  padx = (25,0),
                  sticky  = W,
                  pady = 20)

        #many toilet
        aream = tk.Entry(self.listFramevp,
                            width = 15,
                            justify=CENTER,
                            )
        aream.grid(column = 1, 
                  row = 7,
                  padx = (20,0),
                  pady = 20,
                  sticky  = E)