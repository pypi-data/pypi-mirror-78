from tkinter import (Frame,
                    Tk,
                    Toplevel,
                    StringVar,
                    IntVar,
                    Radiobutton
                    )
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from appnvn.atadctn.icontt import gui
from appnvn.atadctn.menu import menu
from appnvn.atadctn.treectn import scbg
from pynvn.caculate.cacul_cavas import (placereccenter,
                                        setbackdimention,
                                        create_poly_from_tleft_bright)

import re
from pynvn.caculate.ratio import ratio
from pynvn.caculate.coord_point import coordp
from pynvn.caculate.area import area
import string
from appnvn.atadctn.opcus import opcus
from appnvn.atadctn.layouttochoice import layoutchoice

from pynvn.tkinker.packgird import forget,return_gird_pack

class reqbuild(Frame):
        """Customer information"""
        def __init__(self,tktk = None,
                        controller= None,
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
                self.tktk = tktk
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
                self.imagenextlayout = imagenextlayout
                self.imageprelayout = imageprelayout
                self.dirfolder = dirfolder
                self.checkclass = "opcus"
                #gui for data 
                
                self.cavheight_width = [1200,750]
                self.framea = [0,0,450,750,"white"]
                self.frameb = [450,0,750,750,"azure"]

                self.sc = scbg(parent = self,
                                cavheight=self.cavheight_width[1],
                                cavwidth=self.cavheight_width[0],
                                bg = "azure", 
                                bgpr = "#5b9bd5",
                                isonlyaframe= False,
                                framea = self.framea, 
                                frameb = self.frameb 
                                )

                self.height = 6000
                self.width = 7000
                # set back area
                self.w_front =  500
                self.w_back =  500
                self.w_left =  500
                self.w_right =  1000
                # traffice around
                self.wr_front =  1000
                self.wr_back =  1200
                self.wr_left=  1300
                self.wr_right= 500
                self.dis_r = 1000
                self.dis_dim = self.dis_r/3
                self.dis_direc = 400
                # create frame a
                self.listFramevp = self.sc.framea
                # create cavas framea 
                self.canv =  self.sc.canvas
                # create fameb
                self.listFramedr = self.sc.frameb
                # create cavas frameb 
                self.pattern = re.compile("[0-9]")
                # create gui for input from customer 
                self.creategui()
                self.frames = {}
                #azure"""
                self.showframe(nameframe="opcus")
        def show_frame(self, page_name):
                '''Show a frame for the given page name'''
                frame = self.frames[page_name]
                frame.tkraise()

        def creategui(self):
                """Create gui for customer information"""
                row = 0
                col = 0 
                # create title for window
                row = row + 1
                cis = tk.Label(self.listFramevp,
                                text = "Ask The House You Want To Build",
                                anchor="e",
                                font = self.labelfont,
                                bg = self.bglb
                                )
                cis.grid(column = 0, 
                                row  = row,
                                padx = self.padx,
                                columnspan = 4
                                )

                #set Address
                row = row + 1
                add = tk.Label(self.listFramevp,
                                text = "*Building Add:"
                                )
                add.grid(column = 0, 
                        row  = row ,
                        sticky  = "e",
                        padx = self.padx,
                        )

                """ using Combobox"""
                # set Province or city
                self.pc = tk.StringVar() 
                combopc =  ttk.Combobox(self.listFramevp, 
                                        textvariable = self.pc
                                        )
                combopc['values'] = ('Province/City',  
                                        'Dak Lak', 
                                        'Ho Chi Minh', 
                                        'Ha Noi', 
                                        'Dong Nai', 
                                        'Long An'
                                        )

                combopc.current(0)
                combopc.grid(column = 1,
                         row = row,
                         columnspan = 4,
                         sticky  = tk.EW) 

                # set District or Town
                self.dt = tk.StringVar() 
                combodt =  ttk.Combobox(self.listFramevp, 
                                        textvariable = self.dt
                                        )
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
                combodt.grid(column = 1, 
                                row = row, 
                                pady = 10,
                                columnspan = 4,
                                sticky  = tk.EW
                                ) 

                # set Ward/Village
                self.wv = tk.StringVar() 
                combowv =  ttk.Combobox(self.listFramevp, 
                                        textvariable = self.wv,
                                        style = 'custom.TCombobox'
                                        )
                combowv['values'] = ('Ward/Village',  
                                        'Cu pong', 
                                        'Chu Kpo'
                                     )
                combowv.current(0)
                row +=1
                combowv.grid(column = 1, 
                                row = row,
                                columnspan = 4,
                                sticky  = tk.EW
                                ) 
                
                v = tk.StringVar(self.listFramevp, 
                                value='Address Street'
                                )
                self.adde = tk.Entry(self.listFramevp,
                                justify="left",
                                text = v
                                )
                self.adde.bind("<Button-1>", 
                                self.some_callback
                                )
                row +=1
                self.adde.grid(column = 1, 
                        row  = row,
                        sticky  = tk.EW,
                        pady = 10,
                        columnspan = 4
                        )

                #  area
                row = row + 1

                arealb = tk.Label(self.listFramevp,
                        text = "*Building Area:",
                        )
                arealb.grid(column = 0, 
                        row = row,
                        padx = self.padx,
                        sticky  = "e")
                vcmd = (self.register(self.validate_username), "%i", "%P")

                # Width entry 
                self.entryw = tk.Entry(self.listFramevp,
                                        width = 10,
                                        validate="focusout",
                                        validatecommand=vcmd,
                                        invalidcommand=self.print_error)

                self.entryw.insert(tk.END, self.width)
                self.entryw.grid(column = 1, 
                        row = row,
                        sticky  = "w")
                #Width label
                self.lbw = tk.Label(self.listFramevp,
                        text = "Width",
                        )
                self.lbw.grid(column = 2, 
                        row = row,
                        sticky  = "w")
                row += 1
               # height entry 
                self.entryh = tk.Entry(self.listFramevp,
                                        width = 10,
                                        validate="focusout",
                                        validatecommand=vcmd,
                                        invalidcommand=self.print_error)
                self.entryh.insert(tk.END, self.height)
                self.entryh.grid(column = 1, 
                        row = row,
                        sticky  = "w")
                #height label
                self.lbh = tk.Label(self.listFramevp,
                        text = "Height",
                        )
                self.lbh.grid(column = 2, 
                        row = row,
                        sticky  = "w")
                
                # Setback space
                row = row + 1
                sbs = tk.Label(self.listFramevp,
                                text = "Sb Space:",
                                )
                sbs.grid(column = 1, 
                        row = row,
                        sticky  = "w")

                # Front 
                self.etf = tk.Entry(self.listFramevp,
                                justify="left",
                                width = 10,
                                validate="focusout",
                                validatecommand=vcmd,
                                invalidcommand=self.print_error
                                )
                self.etf.grid(column = 2, 
                        row  = row,
                        sticky  = "w",
                        )
                # set defaut value for entry 
                self.etf.insert(tk.END, self.w_front)
                
                self.lbf = tk.Label(self.listFramevp,
                        text = "Front",
                        )
                self.lbf.grid(column = 3, 
                        row = row,
                        sticky  = "w")
                        
                # Back
                row += 1
                self.etb = tk.Entry(self.listFramevp,
                                justify="left",
                                width = 10,
                                validate="focusout",
                                validatecommand=vcmd,
                                invalidcommand=self.print_error
                                )
                self.etb.grid(column = 2, 
                        row  = row,
                        sticky  = "w",
                        )
                # set defaut value for entry 
                self.etb.insert(tk.END, self.w_back)
                
                self.lbb = tk.Label(self.listFramevp,
                        text = "Back",
                        )
                self.lbb.grid(column = 3, 
                        row = row,
                        sticky  = "w")

                # Left
                row += 1
                self.etl = tk.Entry(self.listFramevp,
                                justify="left",
                                width = 10,
                                validate="focusout",
                                validatecommand=vcmd,
                                invalidcommand=self.print_error
                                )
                self.etl.grid(column = 2, 
                        row  = row,
                        sticky  = "w",
                        )
                # set defaut value for entry 
                self.etl.insert(tk.END, self.w_left)
                
                self.lbl = tk.Label(self.listFramevp,
                        text = "Left",
                        )
                self.lbl.grid(column = 3, 
                        row = row,
                        sticky  = "w")        

                #right
                row += 1
                self.etr = tk.Entry(self.listFramevp,
                                justify="left",
                                width = 10,
                                validate="focusout",
                                validatecommand=vcmd,
                                invalidcommand=self.print_error
                                )
                self.etr.grid(column = 2, 
                        row  = row,
                        sticky  = "w",
                        )
                # set defaut value for entry 
                self.etr.insert(tk.END, self.w_right)
                
                self.lbr = tk.Label(self.listFramevp,
                        text = "Right",
                        )
                self.lbr.grid(column = 3, 
                        row = row,
                        sticky  = "w")     
        
                ############traffic 
                row = row + 1
                lb1 = tk.Label(self.listFramevp,
                                text = "Traffic Around:",
                                )
                lb1.grid(column = 0, 
                        row = row,
                        padx = self.padx,
                        sticky  = "e")
                # width of before 
                self.et1 = tk.Entry(self.listFramevp,
                                width = 10,
                                validate="focusout",
                                validatecommand=vcmd,
                                invalidcommand=self.print_error
                                )
                self.et1.grid(column = 1, 
                        row = row,
                        sticky  = "w")
                self.et1.insert(tk.END, self.wr_front)
                #Width of before label 
                self.lbwf = tk.Label(self.listFramevp,
                        text = "W_Font",
                        )
                self.lbwf.grid(column = 2, 
                        row = row,
                        sticky  = "w")
                row += 1
               # height of entry back 
                self.et2 = tk.Entry(self.listFramevp,
                                width = 10,
                                validate="focusout",
                                validatecommand=vcmd,
                                invalidcommand=self.print_error)
                self.et2.grid(column = 1, 
                        row = row,
                        sticky  = "w")
                self.et2.insert(tk.END, self.w_back)
                #height of entry After label
                self.lbwb = tk.Label(self.listFramevp,
                        text = "W_Back",
                        )
                self.lbwb.grid(column = 2, 
                        row = row,
                        sticky  = "w")
                row += 1
                #height of Left entry
                self.et3 = tk.Entry(self.listFramevp,
                                width = 10,
                                validate="focusout",
                                validatecommand=vcmd,
                                invalidcommand=self.print_error)
                self.et3.grid(column = 1, 
                        row = row,
                        sticky  = "w")
                self.et3.insert(tk.END, self.wr_left)
                #height of  Left label
                self.lbwl = tk.Label(self.listFramevp,
                        text = "W_Left",
                        )
                self.lbwl.grid(column = 2, 
                        row = row,
                        sticky  = "w")
                row += 1
                #height of right entry
                self.et4 = tk.Entry(self.listFramevp,
                                width = 10,
                                validate="focusout",
                                validatecommand=vcmd,
                                invalidcommand=self.print_error)
                self.et4.grid(column = 1,
                        row = row,
                        sticky  = "w")
                self.et4.insert(tk.END, self.wr_right)
                #height of  right label
                self.lbwr = tk.Label(self.listFramevp,
                        text = "W_Right",
                        )
                self.lbwr.grid(column = 2, 
                        row = row,
                        sticky  = "w")

                # Traffic
                row += 1
                lb6 = tk.Label(self.listFramevp,
                                text = "*Type House:",
                                )
                lb6.grid(column = 0, 
                        row = row,
                        padx = self.padx,
                        sticky  = "e")
                
                var1 = IntVar()
                rb1 = Radiobutton(self.listFramevp,
                                        text = "Type 1",
                                        variable= var1)
                rb1.grid(column = 1,
                                row  = row,
                                 sticky = "w")

                row += 1
                var2 = IntVar()
                rb2 = Radiobutton(self.listFramevp,
                                text = "Type 2",
                                variable= var2)
                rb2.grid(column = 1,
                                row  = row,
                                sticky = "w")

                row += 1
                var3 = IntVar()
                rb3 = Radiobutton(self.listFramevp,
                                        text = "Type 3",
                                        variable= var3)
                rb3.grid(column = 1,
                                row  = row,
                                 sticky = "w")

                #Scale of ATAD house """
                row = row + 1
                lb7 = tk.Label(self.listFramevp,
                                text = "Util Quantum:",
                                )
                lb7.grid(column = 0, 
                        row = row,
                        padx = self.padx,
                        sticky  = "e")
                # width of before 
                et5 = tk.Entry(self.listFramevp,width = 10)
                et5.grid(column = 1, 
                        row = row,
                        sticky  = "w")

                #Width of before label 
                lb8 = tk.Label(self.listFramevp,
                        text = "Toilet",
                        )
                lb8.grid(column = 2, 
                        row = row,
                        sticky  = "w"
                        )

                row += 1
               # height of entry after 
                et6 = tk.Entry(self.listFramevp,width = 10)
                et6.grid(column = 1, 
                        row = row,
                        sticky  = "w")
                #height of entry After label
                lb9 = tk.Label(self.listFramevp,
                        text = "Bathroom",
                        )
                lb9.grid(column = 2, 
                        row = row,
                        sticky  = "w")
                row += 1
                #height of Left entry
                et7 = tk.Entry(self.listFramevp,width = 10)
                et7.grid(column = 1, 
                        row = row,
                        sticky  = "w"
                        )

                #height of  Left label
                lb10 = tk.Label(self.listFramevp,
                        text = "Bedroom",
                        )
                lb10.grid(column = 2, 
                        row = row,
                        sticky  = "w"
                        )

                row += 1
                #height of right entry
                et8 = tk.Entry(self.listFramevp,width = 10)
                et8.grid(column = 1, 
                        row = row,
                        sticky  = "w")

                #height of  right label
                lb11 = tk.Label(self.listFramevp,
                        text = "Church",
                        )
                lb11.grid(column = 2, 
                        row = row,
                        sticky  = "w"
                        )
                row += 1

                # previous buttons
                self.btpre = tk.Button(self.listFramevp,
                                        image = self.imagepre,
                                        bg = "white",
                                        command = lambda: self.show_frame_control(),
                                        activebackground = "#33B5E5", 
                                        relief = tk.FLAT
                                        )

                self.btpre.grid(column = 1,
                                row = row,
                                columnspan = 1,
                                sticky  = "w",
                                )
                
                # next buttons
                self.btnext = tk.Button(self.listFramevp,
                                        image  = self.imagenext,
                                        bg = "white",
                                        command = lambda: self.showframe(),
                                        activebackground = "#33B5E5", 
                                        relief = tk.FLAT
                                        )
                
                self.btnext.grid(column = 1,
                                row = row,
                                columnspan = 1,
                                sticky  = "e"
                                )
                # click go to layout to choice 
                self.btlabel = tk.Label (self.listFramevp,text = "Click go to layout")
                self.btlabel.grid(column = 2,
                                row = row,
                                sticky  = "e",
                                columnspan = 2
                                )

                # set confg for all (label, combo, entry)"""
                # config label

                labels = (self.lbw,
                                self.lbh,
                                self.lbf,
                                self.lbb,
                                self.lbl,
                                self.lbl,
                                arealb,
                                sbs,
                                self.lbr,
                                add,
                                lb1,
                                self.lbwf,
                                self.lbwb,
                                self.lbwl,
                                self.lbwr,
                                lb6,
                                rb1,
                                rb2,
                                rb3,
                                lb7,
                                lb8,
                                lb9,
                                lb10,
                                lb11,
                                self.btlabel)
                for label in labels:
                        label.config (bg = self.bglb,
                                        font=self.labelfont_sm,
                                        anchor="e")
                
                # config combo
                cobl = (combodt,combopc,combowv)
                for conb in cobl:
                        conb.config (font=self.labelfont_sm)

                # config entry 
                entrys = (self.entryw,
                                self.entryh,
                                self.etf,
                                self.etb,
                                self.etl,
                                self.etr,
                                self.adde,
                                self.et1,
                                self.et2,
                                self.et3,
                                self.et4,
                                et5,
                                et6,
                                et7,
                                et8)
                for entry in entrys:
                        entry.config(font=self.labelfont_sm,
                                        bg = "white",
                                        relief = tk.SOLID)

        def some_callback(self,event): # note that you must include the event as an arg, even if you don't use it.
                """Delete value defaut entry"""
                self.adde.delete(0, "end")
                return None

        def validate_username(self, index, username):
                """validate user name """
                self.getparameter()
                if self.checkclass == "opcus":
                        frame = opcus(tktk=self.listFramedr, 
                                                controller=self,
                                                imagenext=self.imagenext,
                                                imagepre=self.imagepre,
                                                height = self.height ,
                                                width = self.width,
                                                w_front = self.w_front,
                                                w_back = self.w_back,
                                                w_left = self.w_left,
                                                w_right = self.w_right,
                                                wr_front = self.wr_front,
                                                wr_back = self.wr_back ,
                                                wr_left= self.wr_left,
                                                wr_right= self.wr_right,
                                                dis_r = self.dis_r,
                                                dis_dim = self.dis_r/3,
                                                dis_direc = self.dis_direc,
                                                frameb=self.frameb,
                                                imagenextlayout=self.imagenextlayout,
                                                imageprelayout = self.imageprelayout,
                                                dirfolder= self.dirfolder
                                                )
                        frame.grid(row=0,
                                        column=0,
                                        sticky="nsew")
                        return_gird_pack(self.btlabel,
                                        column = 2,
                                        row = 23,
                                        sticky  = "e",
                                        columnspan = 2)

                        return_gird_pack(self.btnext,
                                        column = 1,
                                        row = 23,
                                        sticky  = "e")
                                
                        self.btpre.grid(column = 1,
                                row = 23,
                                columnspan = 1,
                                sticky  = "w",
                                )
                                        
                self.checkclass = "opcus" 
                return self.pattern.match(username) is not None
        def show_frame_control (self,nameframe ="incus"):
                self.btpre.grid(column = 1,
                                row = 23,
                                columnspan = 1,
                                sticky  = "w",
                                )
                
                return_gird_pack(self.btnext,
                                column = 1,
                                row = 23,
                                sticky  = "e"
                                )
                self.controller.show_frame(nameframe)

        def showframe(self, nameframe = "layoutchoice"):
                """ show frame """
                for F in (opcus,layoutchoice):
                        page_name = F.__name__
                        frame = F(tktk=self.listFramedr, 
                                        controller=self,
                                        imagenext=self.imagenext,
                                        imagepre=self.imagepre,
                                        height = self.height ,
                                        width = self.width,
                                        w_front = self.w_front,
                                        w_back = self.w_back,
                                        w_left = self.w_left,
                                        w_right = self.w_right,
                                        wr_front = self.wr_front,
                                        wr_back = self.wr_back ,
                                        wr_left= self.wr_left,
                                        wr_right= self.wr_right,
                                        dis_r = self.dis_r,
                                        dis_dim = self.dis_r/3,
                                        dis_direc = self.dis_direc,
                                        frameb=self.frameb,
                                        imagenextlayout=self.imagenextlayout,
                                        imageprelayout = self.imageprelayout,
                                        dirfolder= self.dirfolder
                                        )
                        self.frames[page_name] = frame
                        frame.grid(row=0,
                                        column=0, 
                                        sticky="nsew")

                if nameframe == "layoutchoice":
                        forget(self.btlabel)
                        forget(self.btnext)
                        self.btpre.grid(column = 1,
                                row = 23,
                                columnspan = 1,
                                sticky  = tk.EW,
                                )
                        self.show_frame("layoutchoice")
                        self.checkclass = "layoutchoice"
                else:
                        self.show_frame("opcus")

        def print_error(self):
                print("Invalid username character, only input number")

        def getparameter(self):                                                
                # width and height of parent area
                
                try:
                        self.height = float(self.entryh.get())
                except:
                        messagebox.showerror("Error",
                                                "check your input {0},\
                                                \nCharacters input must be numbers\
                                                can not string".format(self.lbh["text"]))
                
                try:
                        self.width =float(self.entryw.get()) 
                except:
                        messagebox.showerror("Error",
                                                "check your input {0},\
                                                \nCharacters input must be numbers\
                                                can not string".format(self.lbw["text"]))
                
                # set distance of road and rec
                self.dis_r = max([self.height,self.width])/4
                # set distance of dim 
                self.dis_dim = self.dis_r/2.5
                #set distace of direction 
                self.dis_direc = self.dis_dim
                # set back area
                try:
                        self.w_front =  float(self.etf.get())
                except:
                        messagebox.showerror("Error",
                                                "check your input {0},\
                                                \nCharacters input must be numbers\
                                                can not string".format(self.lbf["text"]))

                try:
                        self.w_back =  float(self.etb.get())
                except:
                        messagebox.showerror("Error","check your input {0},\
                                                \nCharacters input must be numbers\
                                                can not string".format(self.lbb["text"]))
                
                try:
                        self.w_left =  float(self.etl.get())
                except:
                        messagebox.showerror("Error","check your input {0},\
                                                \nCharacters input must be numbers\
                                                 can not string".format(self.lbl["text"]))
                
                try:
                        self.w_right =  float(self.etr.get())

                except:
                        messagebox.showerror("Error","check your input {0},\
                                                \nCharacters input must be numbers\
                                                can not string".format(self.lbr["text"]))          
                # traffice around
                try:
                        self.wr_front =  float(self.et1.get())
                except:
                        messagebox.showerror("Error","check your input {0},\
                                                \nCharacters input must be numbers\
                                                 can not string".format(self.lbwf["text"])) 
                
                try:
                        self.wr_back =  float(self.et2.get())
                except:
                        messagebox.showerror("Error","check your input {0},\
                                                \nCharacters input must be numbers\
                                                can not string".format(self.lbwb["text"])) 
                
                try:
                        self.wr_left=  float(self.et3.get())
                except:
                        messagebox.showerror("Error","check your input {0},\
                                                \nCharacters input must be numbers\
                                                can not string".format(self.lbwl["text"])) 

                try:
                        self.wr_right=  float(self.et4.get())
                except:
                        messagebox.showerror("Error","check your input {0},\
                                                \nCharacters input must be numbers\
                                                 can not string".format(self.lbwr["text"]))


