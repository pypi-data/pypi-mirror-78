
from pynvn.caculate.coord_point import coordp
class directnmwe:
    """ create text direction nmwe"""
    def __init__ (self,canvasb = None,
                                height = 100, 
                                width = 100,
                                dis_r = 0,
                                wr_front = 0,
                                wr_back = 0,
                                wr_left = 0,
                                wr_right = 0,
                                dis_direc = 0,
                                leftpoint = None,
                                rightpoint = None
                                ):
        self.canvasb = canvasb
        self.height = height  
        self.width = width
        self.dis_r = dis_r
        self.wr_front = wr_front
        self.wr_back = wr_back
        self.wr_left = wr_left
        self.wr_right = wr_right
        self.dis_direc = dis_direc
        self.leftpoint = leftpoint
        self.rightpoint = rightpoint

    
    def nsew(self,**kwargs):
        value_dis = self.revalue_dis()

        cp = coordp(topleftp=self.leftpoint,
                                    bottomrightp=self.rightpoint,
                                    dis_direc= self.dis_direc)

        fpc = cp.centerpoinparent()

        frontp = [fpc[0],fpc[1] - value_dis]
        backp = [fpc[0],fpc[1] + value_dis]

        leftp = [fpc[0] - value_dis ,fpc[1]]
        rightp = [fpc[0] + value_dis ,fpc[1]]

        # create text front
        try:
            self.canvasb.delete(self.frf ) # remove
        except:
            pass

        self.frf = self.canvasb.create_text(*frontp, 
                                            anchor="center",
                                            text ="Front", 
                                            angle=0,
                                            **kwargs)
        # create text back
        try:
            self.canvasb.delete(self.frb ) # remove
        except:
            pass

        self.frb = self.canvasb.create_text(*backp, 
                                            anchor="center",
                                            text ="Back", 
                                            angle=0,
                                            **kwargs)
        # create text left
        try:
            self.canvasb.delete(self.frl ) # remove
        except:
            pass

        self.frl = self.canvasb.create_text(*leftp, 
                                            anchor="center",
                                            text ="Left", 
                                            angle=90,
                                            **kwargs)
        # create text right 
        try:
            self.canvasb.delete(self.frr ) # remove
        except:
            pass

        self.frr = self.canvasb.create_text(*rightp, 
                                                anchor="center",
                                                text ="Right", 
                                                angle=-90,
                                                **kwargs)
    def revalue_dis (self):
        self.value_dis = max ([self.height/2 + self.dis_r + self.wr_front+ self.dis_direc, 
                                    self.height/2 + self.dis_r + self.wr_back + self.dis_direc,
                                    self.width/2 + self.dis_r + self.wr_left + self.dis_direc,
                                    self.width/2 + self.dis_r + self.wr_right + self.dis_direc
                                    ])
        return self.value_dis 