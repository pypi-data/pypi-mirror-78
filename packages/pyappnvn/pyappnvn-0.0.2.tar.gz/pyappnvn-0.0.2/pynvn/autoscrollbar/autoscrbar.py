import tkinter as tk

class AutoScrollbar(tk.Scrollbar): 

    """ Defining set method with all  """
    # its parameter 
    
    def set(self, low, high): 

        if float(low) <= 0.0 and float(high) >= 1.0: 

            # Using grid_remove 

            self.tk.call("grid", "remove", self) 

        else: 

            self.grid() 

        tk.Scrollbar.set(self, low, high) 
class autoscrollbarctn:
    """ auto scroll bar for container"""
    def __init__ (self,fameparent = None, canvas = None):
        self.fameparent = fameparent
        self.canvas = canvas
        self.__add_scroll_bars
        self.__addcommmandscroll
        self.__conf

    def __add_scroll_bars(self):

        """add scroll bar """

        # Defining vertical scrollbar 

        self.verscrollbar = AutoScrollbar(self.fameparent) 

        # Calling grid method with all its 

        # parameter w.r.t vertical scrollbar 

        self.verscrollbar.grid(row=0, column=1,sticky=tk.N+tk.S) 

        # Defining horizontal scrollbar 

        self.horiscrollbar = AutoScrollbar(self.fameparent,orient=tk.HORIZONTAL) 

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

        #self.framecv.update_idletasks()

        self.canvas.bind("<Configure>",

                            self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.


    def onFrameConfigure(self, event):                                              

        '''Reset the scroll region to encompass the inner frame'''

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.