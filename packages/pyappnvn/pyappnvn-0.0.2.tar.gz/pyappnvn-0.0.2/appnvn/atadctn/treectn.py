from tkinter import (Frame,
                        Tk,
                        ttk)
from PIL import ImageTk
import tkinter as tk
from pynvn.autoscrollbar.autoscrbar import AutoScrollbar

class cvframe(tk.Frame):

    def __init__(self,cavas = None,

                    anchor = "nw", 

                    createwdx = 10,

                    createwdy = 10):

        self.cavas = cavas

        self.anchor = anchor

        self.createwdx = createwdx

        self.createwdy = createwdy

        tk.Frame.__init__(self,cavas)
        
        self.pack(fill = tk.Y, expand = True)
    

    def rtframecv(self):

        self.listFrame =Frame(self)

        self.cavas.create_window(self.createwdx,

                                self.createwdy,

                                window=self.listFrame,

                                anchor=self.anchor)

        return self.listFrame



class cvframeg:

    """using for gird return listframe"""

    def __init__(self,cavas = None,

                anchor = tk.NW,

                createwdx = 0,

                createwdy = 0,

                cavwidth = 800,

                cavheight = 800,

                bg = "pink"):

        self.cavas = cavas

        self.anchor = anchor

        self.createwdx = createwdx

        self.createwdy = createwdy

        self.bg = bg

        self.cavwidth = cavwidth

        self.cavheight =cavheight

    

    def rtframecv(self):

        """ creating canvas contents """

        self.framecv = Frame(self.cavas,
                            background=self.bg)

        self.window = self.cavas.create_window((self.createwdx,

                                                self.createwdy), 

                                                width=self.cavwidth,

                                                height=self.cavheight,

                                                anchor=self.anchor,

                                                window=self.framecv
                                                ) 

        return self.framecv

class scbg (tk.Frame):

    """ create AutoScrollbar follow gird """

    def __init__ (self,parent = None,
                        bg = "SteelBlue1",
                        bgpr = "red",
                        framea_cw = [10,10],
                        cavwidth = 100,
                        cavheight = 100,
                        isonlyaframe = True,
                        frameincavas = False,
                        frameaincavas = False,
                        framebincavas = False,
                        framecincavas = False,
                        framedincavas = False,
                        **kwargs):
        self.bg = bg
        self.frameincavas = frameincavas

        self.frameaincavas = frameaincavas

        self.framebincavas = framebincavas

        self.framecincavas = framecincavas

        self.framedincavas = framedincavas

        self.kwargs = kwargs

        self.bgpr = bgpr

        self.cavwidth = cavwidth

        self.cavheight =cavheight

        self.framea_cw = framea_cw

        self.isonlyaframe = isonlyaframe

        tk.Frame.__init__(self, parent, bg = self.bgpr)

        self.parent = parent

        self.pack(fill = tk.BOTH, expand = True)

        self.__create_canvas()

        self.__add_scroll_bars()

        self.__addcommmandscroll()

        self.__conf()
        

    def __create_canvas(self):

        """Creating scrolled canvas """

        self.canvas = tk.Canvas(self,

                            bg = self.bg,

                            width=self.cavwidth,

                            height=self.cavheight,

                            highlightcolor = "red",

                            highlightthickness=0,

                            ) 

        self.canvas.grid(row=0, 

                        column=0) 

        # Making the canvas expandable 

        self.grid_rowconfigure(0, weight=1) 

        self.grid_columnconfigure(0, weight=1) 

        if self.isonlyaframe:
                
            cvf = cvframeg(cavas=self.canvas,

                            createwdx=0,
                            
                            createwdy=0,

                            cavheight=self.cavheight ,

                            cavwidth=self.cavwidth,

                            bg=self.bg
                            )

            self.framecv = cvf.rtframecv()

        else:
            framea_k = self.kwargs.get("framea",[0,0,0,0,"white"])
            frameb_k = self.kwargs.get("frameb",[0,0,0,0,"white"])
            framec_k = self.kwargs.get("framec",[0,0,0,0,"white"])
            framed_k = self.kwargs.get("framed",[0,0,0,0,"white"])

            self.framea = cvframeg(cavas=self.canvas,
                                    cavheight=framea_k[3],
                                    cavwidth=framea_k[2],
                                    createwdy=framea_k[1],
                                    createwdx=framea_k[0],
                                    bg=framea_k[4]
                                    ).rtframecv()

            self.frameb = cvframeg(cavas=self.canvas,
                                    bg=frameb_k[4],
                                    cavheight=frameb_k[3],
                                    cavwidth=frameb_k[2],
                                    createwdy=frameb_k[1],
                                    createwdx=frameb_k[0]
                                    ).rtframecv()
            
            self.framec = cvframeg(cavas=self.canvas,
                                    bg=framec_k[4],
                                    cavheight=framec_k[3],
                                    cavwidth=framec_k[2],
                                    createwdy=framec_k[1],
                                    createwdx=framec_k[0]
                                    ).rtframecv()
            self.framed = cvframeg(cavas=self.canvas,
                                    bg=framec_k[4],
                                    cavheight=framed_k[3],
                                    cavwidth=framed_k[2],
                                    createwdy=framed_k[1],
                                    createwdx=framed_k[0]
                                    ).rtframecv()

        if self.frameincavas:

            self.canvas = tk.Canvas(self.framecv,   
                                    width=self.cavwidth,
                                    height=self.cavheight,
                                    bg = self.bg,
                                    highlightthickness=0,
                                    )
            self.canvas.grid(row=0, column=0, sticky=tk.NSEW) 

        if self.frameaincavas:

                # cavas a
                self.canvasa = tk.Canvas(self.framea, 
                                        bg = framea_k[4],
                                        borderwidth=0,
                                        highlightthickness=0)
                self.canvasa.pack(fill = tk.BOTH, 
                                        expand = True) 

        if self.framebincavas:        
                # cavas b
                self.canvasb = tk.Canvas(self.frameb,
                                                bg = frameb_k[4],
                                                borderwidth=0,
                                                highlightthickness=0)
                self.canvasb.pack(fill = tk.BOTH, expand = True) 

        if self.framecincavas:
                # cavas c 
                self.canvasc = tk.Canvas(self.framec, 
                                        bg = framec_k[4],
                                        borderwidth=0,
                                        highlightthickness=0)
                self.canvasc.pack(fill = tk.BOTH, 
                                        expand = True) 

        if self.framedincavas:
                # cavas d
                self.canvasd = tk.Canvas(self.framed, 
                                        bg =framed_k[4],
                                        borderwidth=0,
                                        highlightthickness=0)
                self.canvasd.pack(fill = tk.BOTH, 
                                        expand = True) 

    def __add_scroll_bars(self):

        """add scroll bar """

        # Defining vertical scrollbar 

        self.verscrollbar = AutoScrollbar(self) 

        # Calling grid method with all its 

        # parameter w.r.t vertical scrollbar 

        self.verscrollbar.grid(row=0, column=1,sticky=tk.N+tk.S) 

        # Defining horizontal scrollbar 

        self.horiscrollbar = AutoScrollbar(self,orient=tk.HORIZONTAL) 

        # Calling grid method with all its  

        self.horiscrollbar.grid(row=1, column=0, sticky=tk.E+tk.W) 


    def __addcommmandscroll (self):

        """set and add scroll bar """

        self.canvas.config(xscrollcommand=self.horiscrollbar.set, 

                            yscrollcommand=self.verscrollbar.set)

        self.verscrollbar.config(command=self.canvas.yview) 

        self.horiscrollbar.config(command=self.canvas.xview) 

    def __conf (self):

        """ Configuring canvas """  

        self.canvas.bind("<Configure>",

                            self.onFrameConfigure) #bind an event whenever the size of the viewPort frame changes.


    def onFrameConfigure(self, event):                                              

        '''Reset the scroll region to encompass the inner frame'''

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))#whenever the size of the frame changes, alter the scroll region respectively.

class autoscrbarn:
    def __init__(self, parent = None, canvas = None,**kwargs):
        self.parent = parent
        self.canvas = canvas

    def __add_scroll_bars(self):

        """add scroll bar """

        # Defining vertical scrollbar 

        self.verscrollbar = AutoScrollbar(self.parent) 

        # Calling grid method with all its 

        # parameter w.r.t vertical scrollbar 

        self.verscrollbar.grid(row=0, column=1,sticky=tk.N+tk.S) 

        # Defining horizontal scrollbar 

        self.horiscrollbar = AutoScrollbar(self.parent,orient=tk.HORIZONTAL) 

        # Calling grid method with all its  

        self.horiscrollbar.grid(row=1, column=0, sticky=tk.E+tk.W) 


    def __addcommmandscroll (self):

        """set and add scroll bar """

        self.canvas.config(xscrollcommand=self.horiscrollbar.set, 

                            yscrollcommand=self.verscrollbar.set)

        self.verscrollbar.config(command=self.canvas.yview) 

        self.horiscrollbar.config(command=self.canvas.xview) 


    def __conf (self):
        """ Configuring canvas """  
        self.canvas.bind("<Configure>",
                            self.onFrameConfigure) #bind an event whenever the size of the viewPort frame changes.
    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))#whenever the size of the frame changes, alter the scroll region respectively.


class scrollbarvn(tk.Frame):
    """ create list check box"""
    def __init__(self, parent,bg = "blue"):
        self.bg = bg
        tk.Frame.__init__(self, parent)
        self.pack(fill = tk.BOTH, expand = True)
        self.vars = []
        self.__create_canvas()
        self.__add_scroll_bars()
        self.__addcommmandscroll()
        self.__conf()
        self.__creframe()
        self.__scrobarforcontrol()
    
    def __creframe (self):
        self.frame = tk.Frame(self.canvas)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.canvas.create_window(0, 0, anchor=tk.NW, window=self.frame)

    def __create_canvas(self):
        """Creating scrolled canvas """

        self.canvas = tk.Canvas(self,
                                highlightthickness=0,
                                bg = self.bg
                            ) 
        self.canvas.grid(row=0,column=0, sticky =  tk.NSEW) 

        # Making the canvas expandable 

        self.grid_rowconfigure(0, weight=1) 

        self.grid_columnconfigure(0, weight=1) 

    def __add_scroll_bars(self):

        """add scroll bar """
        # Defining vertical scrollbar 
        self.verscrollbar = AutoScrollbar(self) 
        # Calling grid method with all its 
        # parameter w.r.t vertical scrollbar 
        self.verscrollbar.grid(row=0, column=1,sticky=tk.N+tk.S) 
        # Defining horizontal scrollbar 
        self.horiscrollbar = AutoScrollbar(self,orient=tk.HORIZONTAL) 
        # Calling grid method with all its  
        self.horiscrollbar.grid(row=1, column=0, sticky=tk.E+tk.W) 


    def __addcommmandscroll (self):
        """set and add scroll bar """
        self.canvas.config(xscrollcommand=self.horiscrollbar.set, 
                            yscrollcommand=self.verscrollbar.set)

        self.verscrollbar.config(command=self.canvas.yview) 
        self.horiscrollbar.config(command=self.canvas.xview) 

    def __conf (self):
        """ Configuring canvas """  
        self.canvas.bind("<Configure>",
                            self.onFrameConfigure) #bind an event whenever the size of the viewPort frame changes.
    
    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))#whenever the size of the frame changes, alter the scroll region respectively.
           
    def __scrobarforcontrol(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")