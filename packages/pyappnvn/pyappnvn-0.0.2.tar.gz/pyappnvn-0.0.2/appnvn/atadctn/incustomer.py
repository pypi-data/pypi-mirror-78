from tkinter import (Frame,
                        Tk,
                        StringVar,
                        Toplevel,
                        IntVar,
                        Radiobutton)
import tkinter as tk
from tkinter import ttk
from appnvn.atadctn.icontt import gui
from appnvn.atadctn.menu import menu
from appnvn.atadctn.treectn import scbg
from appnvn.atadctn.reqbuild import reqbuild

class incus(Frame):
        """ customer information"""
        def __init__(self,tktk = None,
                        controller = None,
                        br_image = None,
                        pathico = None,
                        br_image_path = None,
                        logoicon = None,
                        bglb = "white",
                        labelfont = ('times', 20),
                        labelfont_sm = ('times', 16),
                        padx = (10,0),
                        imagenext = None,
                        imagepre = None,
                        imagenextlayout = None,
                        imageprelayout = None,
                        dirfolder = None
                        ):
                
                Frame.__init__(self, tktk)
                self.controller = controller
                self.labelfont = labelfont
                self.labelfont_sm = labelfont_sm
                self.br_image_path  = br_image_path
                self.br_image = br_image
                self.logoicon = logoicon
                self.padx = padx
                self.pathico = pathico
                self.bglb = bglb
                self.imagenext = imagenext
                self.imagepre = imagepre
                self.dirfolder = dirfolder
                self.pack()
                #gui for data 
                self.sc = scbg(parent = self,
                                cavheight=600,
                                cavwidth=600,
                                bg = "white", 
                                bgpr = "#5b9bd5")
                
                self.listFramevp = self.sc.framecv
                self.canv =  self.sc.canvas
                self.creategui()
        def creategui(self):
                """create gui for customer information"""
                #image logo
                row = 0
                col = 0 
                logolbl = tk.Label (self.listFramevp,
                                image = self.logoicon,
                                borderwidth=0,
                                compound="center",
                                highlightthickness = 0)

                logolbl.grid (row = row,
                                pady = 10,
                                columnspan = 4)
                
                #line 1
                ci = tk.Label(self.listFramevp,
                                text = "Customer info:"
                                )
                row = row + 1
                ci.grid(column = 0, 
                        row = row,
                        padx = self.padx,
                        sticky  = tk.W)
                
                #Line 2
                row = row + 1
                cis = tk.Label(self.listFramevp,
                                text = "Thanks for your interest in getting a ATAD HOUSE"
                                )
                cis.grid(column = 0, 
                                row  = row ,
                                padx = self.padx,
                                sticky  = "w",
                                columnspan = 4
                                )

                #  full name
                row = row + 1
                
                fn = tk.Label(self.listFramevp,
                        text = "*Your Name:",
                        )
                fn.grid(column = 0, 
                        row = row,
                        padx = self.padx,
                        sticky  = tk.W)
                
                fn.config (bg = self.bglb)
                fn.config(font=self.labelfont_sm)
                #row = row + 1
                col = col + 1
                fne = tk.Entry(self.listFramevp,
                                justify="left",
                                text = "Nguyen Van Nhuan"
                                )
                fne.grid(column = 1, 
                        row  = row,
                        columnspan = 3,
                        sticky  = tk.EW,
                        )

                # Phone Number
                row = row + 1
                pn = tk.Label(self.listFramevp,text = "*Phone Number:",
                                )
                pn.grid(column = 0, 
                        row = row,
                        padx = self.padx,
                        sticky  = tk.W)

                pne = tk.Entry(self.listFramevp,
                                justify="left",
                                text = "Nguyen Van Nhuan"
                                )
                pne.grid(column = 1, 
                        row  = row,
                        sticky  = tk.EW,
                        columnspan = 3,
                        )
                
                #email 
                em = tk.Label(self.listFramevp,
                                text = "*Email:",
                                )
                row = row + 1
                em.grid(column = 0, 
                        row  = row ,
                        sticky  = "w",
                        padx = self.padx,
                        )

                eme = tk.Entry(self.listFramevp,
                                justify="left",
                                text = "Nguyen Van Nhuan"
                                )
                eme.grid(column = 1, 
                        row  = row,
                        columnspan = 3,
                        sticky  = tk.EW 
                        )

                #Gender
                gd = tk.Label(self.listFramevp,
                                text = "*Gender:",
                                )
                row = row + 1
                gd.grid(column = 0, 
                        row  = row ,
                        sticky  = "w",
                        padx = self.padx,
                        )

                var1 = IntVar()
                ckgender = Radiobutton(self.listFramevp,
                                        text = "Male",
                                        variable= var1)
                ckgender.grid(column = 1,
                                row  = row)

                var2 = IntVar()
                ckgender2 = Radiobutton(self.listFramevp,
                                        text = "Female",
                                        variable= var2)
                ckgender2.grid(column = 2,
                                row  = row)

                #set Address
                row = row + 1
                add = tk.Label(self.listFramevp,
                                text = "*Address:"
                                )
                add.grid(column = 0, 
                        row  = row ,
                        sticky  = "w",
                        padx = self.padx,
                        )

                # set Province or city
                self.pc = tk.StringVar() 
                combopc =  ttk.Combobox(self.listFramevp, textvariable = self.pc)
                combopc['values'] = ('Province/City',  
                                ' Dak Lak', 
                                ' Ho Chi Minh', 
                                ' Ha Noi', 
                                ' Dong Nai', 
                                ' Long An'
                                )

                combopc.current(0)
                combopc.grid(column = 1, row = row,columnspan = 4,sticky  = tk.EW) 
                # set District or Town
                self.dt = tk.StringVar() 
                combodt =  ttk.Combobox(self.listFramevp, textvariable = self.dt)
                combodt['values'] = ('District/Town',  
                                'Krong Buk', 
                                'Buon Ho', 
                                'Ehleo', 
                                '1 District', 
                                '2 District', 
                                '3 District', 
                                '4 District'
                                ) 
                combodt.current(0)
                row = row + 1
                combodt.grid(column = 1, row = row, pady = 10,columnspan = 4,sticky  = tk.EW) 

                # set Ward/Village
                self.wv = tk.StringVar() 
                combowv =  ttk.Combobox(self.listFramevp, 
                                        textvariable = self.wv,style = 'custom.TCombobox')
                combowv['values'] = ('Ward/Village',  
                                ' Cu pong', 
                                ' Chu Kpo'
                                ) 
                combowv.current(0)
                row +=1
                combowv.grid(column = 1, row = row,columnspan = 4,sticky  = tk.EW) 

                v = StringVar(self.listFramevp, value='Address Street')
                self.adde = tk.Entry(self.listFramevp,
                                justify="left",
                                text = v
                                )
                self.adde.bind("<Button-1>", self.some_callback)
                row +=1
                self.adde.grid(column = 1, 
                        row  = row,
                        sticky  = tk.EW,
                        pady = 10,
                        columnspan = 4
                        )

                #Year of Birth
                yb = tk.Label(self.listFramevp,
                                text = "*Year of Birth:",
                                )
                row +=1
                yb.grid(column = 0, 
                        row = row,
                        padx = self.padx,
                        sticky  = tk.EW)
                # set day
                self.sd = tk.StringVar() 
                comboday =  ttk.Combobox(self.listFramevp, 
                                        textvariable = self.sd,
                                        style = 'custom.TCombobox',
                                        width=9)
                dayl = ["Day"] + list(range(1,32))
                comboday['values'] = dayl
                comboday.current(0)
                comboday.grid(column = 1, 
                                row = row,
                                sticky  = tk.EW) 

                # set month
                
                self.sm = tk.StringVar() 
                combom =  ttk.Combobox(self.listFramevp, 
                                        textvariable = self.sm,
                                        style = 'custom.TCombobox',
                                        width=9)
                mothl = ["Month"] + list(range(1,13))
                combom['values'] = mothl
                combom.current(0)
                #row +=1
                combom.grid(column = 2, 
                                row = row,
                                sticky  = tk.EW) 
                
                # set year
                
                self.sy = tk.StringVar() 
                comboy =  ttk.Combobox(self.listFramevp, 
                                        textvariable = self.sy,
                                        style = 'custom.TCombobox',
                                        width=9)
                yearl = ["Year"] + list(range(1900,2021))
                comboy['values'] = yearl
                comboy.current(0)
                #row +=1
                comboy.grid(column = 3, 
                                row = row,
                                sticky  = tk.EW) 
                # button next
                
                button1 = tk.Button(self.listFramevp, 
                                text = "Next",
                                bg = "azure2",
                                image = self.imagenext,
                                relief = tk.FLAT,
                                compound = tk.LEFT,
                                command= lambda:self.controller.show_frame("reqbuild"),
                                font = ("times new roman",20)
                                )
                row +=1
                button1.grid (column = 0, 
                                row = row,
                                columnspan = 4,
                                padx = self.padx,
                                pady = 10,
                                sticky  = tk.EW)
        
                # config label
                labels = (ci,gd,cis,fn,add,pn,em,yb,ckgender,ckgender2)
                for label in labels:
                        label.config (bg = self.bglb,
                                        font=self.labelfont,
                                        anchor="w")
                # set combo
                cobl = (combowv,combodt,combopc,comboday,combom,comboy)
                for conb in cobl:
                        conb.config (font=self.labelfont_sm)
                        
                # config entry 
                entrys = (fne,pne,eme, self.adde)
                for entry in entrys:
                        entry.config(font=self.labelfont_sm,
                                        bg = "white",
                                        relief = tk.SOLID)
                
                
        def buttomandnext (self, image = None,text = None, cavx = 0,cavy = 0):

                button1 = Button(self.canv, 
                                bg = "white",
                                image = self.imagenext
                                )
                button1.configure(width = 100, 
                                activebackground = "#33B5E5", 
                                relief = tk.FLAT)
                button1_window = self.canv.create_window(cavx, cavy, 
                                                        anchor=tk.NW, 
                                                        window=button1)

        """delete value defaut entry """
        def some_callback(self,event): # note that you must include the event as an arg, even if you don't use it.
                self.adde.delete(0, "end")
                return None
