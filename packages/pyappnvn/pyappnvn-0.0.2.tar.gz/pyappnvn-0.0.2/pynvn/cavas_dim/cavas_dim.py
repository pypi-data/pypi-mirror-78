class dimrec:
    """ create text and arrow"""
    def __init__ (self, cavas = None, 
                    locationtext = [0,0],
                    locationarrow =[100,100], 
                    text = None,
                    angle = 0):

        self.cavas = cavas
        self.locationtext = locationtext
        self.locationarrow = locationarrow
        self.text = text
        self.angle = angle
    def createarrow (self):
        try:

            self.cavas.delete(self.rll ) # remove
        except:
            pass

        self.rll = self.cavas.create_line(*self.locationarrow,
                                                        fill = "red",
                                                        arrow = "both"
                                                        )
    
    def createtext(self):
        """create text """
        try:

                self.cavas.delete(self.cvt ) # remove
        except:
                pass

        self.cvt = self.cavas.create_text(*self.locationtext, 
                                                        anchor="n",
                                                        text =self.text , 
                                                        angle=self.angle
                                                        )