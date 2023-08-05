from tkinter import *
import tkinter as tk
from pynvn.path.ppath import PathFromFileNameAndDirpath
from appnvn.atadctn.indatatosel import indatagui
from appnvn.atadctn.choicelayout import layoutgui
from appnvn.atadctn.spsquotation import spreadsheetgui
import tkinter.font as font
from appnvn.atadctn.menu import menu
from appnvn.atadctn.icontt import gui
class selop:
    def __init__(self,tktk = None, 
                    br_image = None,
                    pathico = None,
                    br_image_path = None,
                    ):

        self.tktk = tktk
        self.br_image = br_image
        self.pathico = pathico
        self.br_image_path = br_image_path


        filewin = Toplevel(self.tktk) 
        gui (tktk=filewin,
                    pathico=self.pathico,
                    width=700,
                    height=450,
                    widthx=700,
                    widthy=0,
                    resizable=[True,True]).setcfbs()
        menu (tktk=filewin).createmenu()

        self.container = Frame (filewin,
                            bg="white")
        
        self.container.pack(fill = BOTH, expand = True)
        
    # create gui     
    def creategui(self):
        # set font siza for text 
        myFont = font.Font(size=30)
        #create buttom for open file 
        button = tk.Button(self.container,text = "INPUT DATA",
                            background = "skyblue2", fg = "white",
                            command = lambda: indatagui(tktk=self.tktk,
                                                        br_image=self.br_image,
                                                        pathico=self.pathico,
                                                        br_image_path=self.br_image_path).creategui()
                            )
        button['font'] = myFont 
        button.pack(fill = BOTH, expand = True)

        button = tk.Button(self.container,text = "CHOOSE LAYOUT",
                            background = "blue", fg = "white",
                            command = lambda: layoutgui(tktk=self.tktk,
                                                        pathico=self.pathico,
                                                        br_image_path=self.br_image_path).creategui()
                            )
        button['font'] = myFont 
        button.pack(fill = BOTH, expand = True)
        
        button = tk.Button(self.container,text = "ADD QUOTATION",
                            background = "green", fg = "white",
                            command = lambda: spreadsheetgui(tktk=self.tktk,
                                                        pathico=self.pathico,
                                                        br_image_path=self.br_image_path)
                            )
        button['font'] = myFont 
        button.pack(fill = BOTH, expand = True)

        button = tk.Button(self.container,text = "EXIT",
                            background = "red", fg = "white",
                            command = lambda: self.container.quit()
                            )
        button['font'] = myFont 
        button.pack(fill = BOTH, expand = True)
