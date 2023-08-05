from pynvn.caculate.area import area
class writetext:
    def __init__ (self,canvas =None,
                topleftkid = None,
                toprightkid = None,
                centerpoint = [0,0]
                ):
        self.canvas = canvas
        self.centerpoint = centerpoint
        self.topleftkid = topleftkid
        self.toprightkid = toprightkid
        

    def warea(self,**kwargs):
        """ write area """

        are_k = area(topleftpoint= self.topleftkid, 
                                bottomrightpoint=self.toprightkid).areafromtopbottompoint()

        # create text 
        try:
            self.canvas.delete(self.tca ) # remove
        except:
            pass
        #coordrcenter = self.coord.centerpointkid()

        self.tca = self.canvas.create_text(*self.centerpoint, 
                                                        anchor="center",
                                                        text ="Area to build: {}".format(are_k), 
                                                        angle=0,
                                                        **kwargs)
        