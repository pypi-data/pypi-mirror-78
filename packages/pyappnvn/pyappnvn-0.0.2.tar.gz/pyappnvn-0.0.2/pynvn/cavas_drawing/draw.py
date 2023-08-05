import tkinter as tk

class dcavas:
    def __init__ (self, 
                    cavas = None, 
                    topp = None, 
                    bottomp = None):
        self.__cavas = cavas
        self.__topp = topp
        self.__bottomp = bottomp
    def drec (self, **kwargs):
        """ drawing rectangle"""
        try:

            self.__cavas.delete(self.rrectangle_kid ) # remove
        except:

            pass
        self.rrectangle_kid = self.__cavas.create_rectangle (*self.__topp,
                                                            *self.__bottomp,**kwargs)
    """
    def dimage(self):
        # put image in to layout 
        bg_icon = tk.PhotoImage(file=r"D:\5.ATADRD\CTNATAD\ctn_image\01.jpg")
        # put gif image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10
        self.__cavas.create_image(100, 100, image=bg_icon, anchor=tk.NW)
    """