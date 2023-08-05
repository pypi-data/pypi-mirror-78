import tkinter as tk # python 3
from appnvn.atadctn.incustomer import incus
from appnvn.atadctn.reqbuild import reqbuild
from appnvn.atadctn.icontt import gui
from appnvn.atadctn.menu import menu
class apppr(tk.Frame):
    def __init__(self, tktk = None, 
                    br_image=None, 
                    pathico=None,
                    br_image_path=None,
                    logoicon=None,
                    imagenext=None,
                    imagepre=None,
                    imagenextlayout = None,
                    imageprelayout = None,
                    dirfolder = None,
                    pathclayout = None,
                    *args, 
                    **kwargs):
        self.tktk = tktk
        self.br_image = br_image
        self.pathico = pathico
        self.br_image_path = br_image_path
        self.logoicon = logoicon
        self.imagenext = imagenext
        self.imagepre = imagepre
        self.imagenextlayout = imagenextlayout
        self.imageprelayout = imageprelayout
        self.dirfolder = dirfolder
        tk.Frame.__init__(self,tktk)
        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.filewin = tk.Toplevel(self.tktk)
        container = tk.Frame(self.filewin,
                            bg = "white")
        container.pack(side="top",
                        fill="both", 
                        expand=True)
        
        container.grid_rowconfigure(0, 
                                    weight=1)
        container.grid_columnconfigure(0, 
                                        weight=1)
        gui (tktk=self.filewin,
                        pathico=self.pathico,
                        width=800,
                        height=800,
                        widthx="center",
                        widthy="center",
                        condv=2.7,
                        resizable=[True,True]).setcfbs()
                
        # set menu 
        menu (tktk=self.filewin,
                pathicon=pathico, 
                pathclayout = pathclayout).createmenu()
        self.frames = {}
        for F in (incus,reqbuild):
            page_name = F.__name__
            frame = F(tktk=container, 
                    controller=self,
                    br_image=self.br_image, 
                    pathico=self.pathico,
                    br_image_path=self.br_image_path,
                    logoicon=self.logoicon,
                    imagenext=self.imagenext,
                    imagepre=self.imagepre,
                    imagenextlayout = self.imagenextlayout,
                    imageprelayout= self.imageprelayout,
                    dirfolder = self.dirfolder)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0,
                        column=0, 
                        sticky="nsew")
        self.show_frame("incus")
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()