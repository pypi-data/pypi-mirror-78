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
from tkintertable import TableCanvas, TableModel

import string


def n2a(n,b=string.ascii_uppercase):
   d, m = divmod(n,len(b))
   return n2a(d-1,b)+b[m] if d else b[m]


def createData(rows=200, cols=50):
        """Creare random dict for test data"""

        data = {}
        names = list (range(0,rows))
        colnames = [n2a(i) for i in range(1,cols + 10) ]
        
        for n in names:
                data[n]={}
                data[n]['A'] = ""
        
                
        for c in range(0,cols):
                colname=colnames[c]
                i=0
                for n in names:
                        data[n][colname] = ""
                        i+=1
        return data


class spreadsheetgui(Frame):

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
                        
                # set data
                data = createData()
                menu (tktk=self.filewin).createmenu()

                #create label 
                self.framelb = Frame(self.filewin,bg = "slate gray")
                self.framelb.pack(side = TOP)

                #creare frame for infomation
                self.frameinfor = Frame(self.filewin,bg = "slate gray")
                self.frameinfor.pack(side = TOP)


                #create title 
                self.framett = Frame(self.filewin,bg = "slate gray")
                self.framett.pack(side = TOP)

                # creare frame for table  
                self.tframe = Frame(self.filewin)
                self.tframe.pack(fill = X,side = TOP)

                model = TableModel()
                table = TableCanvas(self.tframe, model=model,data=data,height=650)
                table.show()

               #update quotation
                self.frameupdate = Frame(self.filewin,bg = "slate gray")
                self.frameupdate.pack(side = TOP)
                
                # import and export excel 
                self.frameimeex = Frame(self.filewin,bg = "slate gray")
                self.frameimeex.pack(side = TOP)


                self.createguiin()

        def createguiin(self):

                #create label
                addlb = tk.Label(self.framelb,text = "QUOTATION FOR CONTAINER")
                addlb.config(font=("Courier", 24))
                addlb.pack()
                #create title 
                crtt = tk.Label(self.framett,text = "QUOTATION")
                crtt.config(font=("Courier", 15))
                crtt.pack(fill = X)

                # create information       
                add = tk.Label(self.frameinfor,text = "Add:",
                                anchor="center",
                                width = 15,
                                height = 1,
                                )
                add.grid(column = 0, 
                        row = 0,
                        pady = 10,
                        padx = 10,

                        )

                #input price
                add = tk.Entry(self.frameinfor,
                                width = 30,
                                justify="center",
                                text = "Zamboanga, Philippines"
                                )
                add.grid(column = 1, 
                        row  = 0 ,
                        ipady = 1
                        )
                
                #  ITEM

                add = tk.Label(self.frameinfor,text = "Tem:",
                                anchor="center",
                                width = 15,
                                height = 1,
                                )
                add.grid(column = 2, 
                        row = 0,
                        pady = 10,
                        padx = 10,
                        )

                add = tk.Entry(self.frameinfor,
                                width = 30,
                                justify="center",
                                text = "PRE-ENGINEERED STEEL BUILDING"
                                )
                add.grid(column = 3, 
                        row  = 0 ,
                        ipady = 1
                        )
                # date
                
                add = tk.Label(self.frameinfor,text = "Date:",
                                anchor="center",
                                width = 15,
                                height = 1,
                                )
                add.grid(column = 4, 
                        row = 0,
                        pady = 10,
                        padx = 10,
                        )

                add = tk.Entry(self.frameinfor,
                                justify="center",
                                width = 30,
                                text = "08/04/2020"
                                )
                add.grid(column = 5, 
                        row  = 0 ,
                        ipady = 1
                        )

                
                #   BOQ type
                
                add = tk.Label(self.frameinfor,text = "BOQ type:",
                                anchor="center",
                                width = 15,
                                height = 1,
                                )
                add.grid(column = 6, 
                        row = 0,
                        pady = 10,
                        padx = 10,
                        )

                add = tk.Entry(self.frameinfor,
                                width = 30,
                                justify="center",
                                text = "Lump sum"
                                )
                add.grid(column = 7, 
                                row  = 0 ,
                                ipady = 1
                                )

                
                # line 2 
                #   BOQ type
                
                add = tk.Label(self.frameinfor,text = "Contact person:",
                                anchor="center",
                                width = 15,
                                height = 1,
                                )
                add.grid(column = 0, 
                        row = 1,
                        pady = 10,
                        padx = 10
                        )


                add = tk.Entry(self.frameinfor,
                                width = 30,
                                justify="center",
                                text = "LRenante Bendana"
                                )
                add.grid(column = 1, 
                                row  = 1 ,
                                padx = 1,
                                )

                # Phone
                
                add = tk.Label(self.frameinfor,text = "Contact person:",
                                anchor="center",
                                width = 15,
                                height = 1,
                                )
                add.grid(column = 2, 
                        row = 1,
                        pady = 10,
                        padx = 10)

                add = tk.Entry(self.frameinfor,
                                width = 30,
                                justify="center",
                                text = "+63 966 483 5871"
                                )
                add.grid(column = 3, 
                                row  = 1,
                                ipady = 1
                                )

                
                #   Office
                
                add = tk.Label(self.frameinfor,text = "Office:",
                                anchor="center",
                                width = 15,
                                height = 1,
                                )
                add.grid(column = 4, 
                        row = 1,
                        pady = 10,
                        padx = 10)

                add = tk.Entry(self.frameinfor,
                                width = 30,
                                justify="center",
                                text = "99 Nguyen Thi Minh Khai, Ben Thanh W, Dist 1, HCMC"
                                )
                add.grid(column = 5, 
                                row  = 1,
                                ipady = 1
                                )

                #   CHECKCHECK
                
                add = tk.Label(self.frameinfor,text = "CHECK:",
                                anchor="center",
                                width = 15,
                                height = 1,
                                )
                add.grid(column = 6, 
                        row = 1,
                        pady = 10,
                        padx = 10)

                add = tk.Entry(self.frameinfor,
                                width = 30,
                                justify="center",
                                text = "TTT"
                                )
                add.grid(column = 7, 
                                row  = 1,
                                ipady = 1
                                )
                #line 3
                
                # DONE
                
                add = tk.Label(self.frameinfor,text = "DONE:",
                                anchor="center",
                                width = 15,
                                height = 1,
                                )
                add.grid(column = 0, 
                        row = 2,
                        pady = 10,
                        padx = 10)

                add = tk.Entry(self.frameinfor,
                                width = 30,
                                justify="center",
                                text = "LAHP"
                                )
                add.grid(column = 1, 
                                row  = 2,
                                ipady = 1
                                )

                #   BOQ expired date
                
                add = tk.Label(self.frameinfor,text = "BOQ expired date:",
                                anchor="center",
                                width = 15,
                                height = 1,
                                )
                add.grid(column = 2, 
                        row = 2,
                        pady = 10,
                        padx = 10)

                add = tk.Entry(self.frameinfor,
                                width = 30,
                                justify="center",
                                text = "within 30 days"
                                )
                add.grid(column = 3, 
                                row  = 2 ,
                                padx = 1,
                                )

                #  QUANTITY CONTAINER
                
                add = tk.Label(self.frameinfor,text = "Quantity Container",
                                anchor="center",
                                width = 15,
                                height = 1,
                                )
                add.grid(column = 4, 
                        row = 2,
                        pady = 10,
                        padx = 10)

                add = tk.Entry(self.frameinfor,
                                width = 30,
                                justify="center",
                                text = "3"
                                )
                add.grid(column = 5, 
                                row  = 2,
                                ipady = 1
                                )

                #  QUANTITY Toilet
                
                add = tk.Label(self.frameinfor,text = "Quantity Toilet",
                                anchor="center",
                                width = 15,
                                height = 1,
                                )
                add.grid(column = 6, 
                        row = 2,
                        pady = 10,
                        padx = 10,)

                add = tk.Entry(self.frameinfor,
                                width = 30,
                                justify="center",
                                text = "3"
                                )
                add.grid(column = 7, 
                                row  = 2,
                                ipady = 1
                                )

                # line 4
                #  QUANTITY Toilet
                
                add = tk.Label(self.frameinfor,text = "Quantity bedroom:",
                                anchor="center",
                                width = 15,
                                height = 1,
                                )
                add.grid(column = 0, 
                        row = 3,
                        pady = 10,
                        padx = 10,)

                add = tk.Entry(self.frameinfor,
                                width = 30,
                                justify="center",
                                text = "3"
                                )
                add.grid(column = 1, 
                                row  = 3,
                                ipady = 1
                                )

                #update excel file
                fameupdatee = tk.Button(self.frameupdate, text = "UPDATE QUOTATION")
                fameupdatee.pack(side = TOP )

                #import and export excel 
                importex = tk.Button(self.frameimeex,
                                        text = "IMPORT FROM EXCEL")
                importex.pack(side = LEFT)
                importex = tk.Button(self.frameimeex,
                                        text = "EXPORT TO EXCEL")
                importex.pack(side = LEFT)