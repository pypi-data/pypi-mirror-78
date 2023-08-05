from pynvn.list.twolist import towlist
class placereccenter:
    """ place center window cavas"""
    def __init__ (self,info_width_P = 100,
                    info_height_p = 100,
                    info_width_k = 100,
                    info_height_k = 100,
                    startpoint = [0,0]):

                self.startpoint = startpoint
                self.info_width_P = info_width_P
                self.info_height_p = info_height_p
                self.info_width_k = info_width_k
                self.info_height_k = info_height_k


    def pointleftrec (self):
        """ return point rectangle on the left"""
        return towlist(self.pointcenterofparent(),
                                    [self.info_width_k/2, 
                                    self.info_height_k/2
                                    ]
                                    ).subtracttowlist()

    def pointrightrec(self):
        """ return point rectangle on the left""" 
        return towlist(self.pointcenterofparent(),
                                    [self.info_width_k/2, 
                                    self.info_height_k/2
                                    ]
                                    ).plustracttowlist()

    def pointcenterofparent (self):
        """ point center of window parent"""
        return towlist(self.startpoint,
                                    [self.info_width_P/2,
                                    self.info_height_p/2
                                    ]
                                    ).plustracttowlist()


class setbackdimention:
    """set back dimention from rectangle"""
    def __init__ (self,w_front = 100,
                    w_back = 100,
                    w_left = 100,
                    w_right = 100,
                    topleftpoint_p = [0,0],
                    bottomrightpoint_p = [100,100]):
                self.w_front = w_front
                self.w_back = w_back
                self.w_left = w_left
                self.w_right = w_right
                self.topleftpoint_p = topleftpoint_p
                self.bottomrightpoint_p = bottomrightpoint_p
    
    def topleftpoint(self):
        """ return top left of window kid"""
        return towlist (list1= self.topleftpoint_p,
                list2= [self.w_left,self.w_front]).plustracttowlist()

    def toprightpoint(self):
        """ return top right of window kid"""
        return towlist (list1= self.bottomrightpoint_p,
                        list2= [self.w_right,self.w_back]).subtracttowlist()

class create_poly_from_tleft_bright:
    """create polygon from top lelf and bottom right """
    def __init__ (self,topleftpoint_p = [0,0],
                    bottomrightpoint_p = [100,100],
                    w_front_r = 100,
                    w_back_r = 100,
                    w_left_r = 100,
                    w_right_r = 100,
                    dis_r = 200
                    ):
                    self.topleftpoint_p = topleftpoint_p
                    self.bottomrightpoint_p = bottomrightpoint_p
                    self.w_front_r = w_front_r
                    self.w_back_r = w_back_r
                    self.w_left_r = w_left_r
                    self.w_right_r = w_right_r
                    self.dis_r = dis_r
    
    def roadfront (self):
        """ create section road front"""
        self.xy1f = [self.topleftpoint_p[0],
                self.topleftpoint_p[1] - self.dis_r
                ]
        self.xyaf= cresectionpoint(point1=self.xy1f,width= self.w_front_r)
        
        self.xy2f = [self.xy1f[0],
                self.xy1f[1] -self.w_front_r
                ]

        self.xy3f = [self.bottomrightpoint_p[0], 
                self.xy2f[1]
                ]
        self.xybf = cresectionpoint(point1=self.xy3f,width= self.w_front_r,direction="y_right")

        self.xy4f = [self.xy3f[0],
                self.xy1f[1]
                ]
        return [*self.xy1f,*self.xyaf,*self.xy2f,*self.xy3f,*self.xybf,*self.xy4f]

    def roadback(self):
        """ create section road back"""
        self.xy1b = [self.bottomrightpoint_p[0],
                self.bottomrightpoint_p[1] + self.dis_r]

        self.xyab = cresectionpoint(point1=self.xy1b,width= self.w_back_r,direction="y_right")

        self.xy2b = [self.xy1b[0],self.xy1b[1] + self.w_back_r]


        self.xy3b = [self.topleftpoint_p[0], self.xy2b[1]]

        self.xybb = cresectionpoint(point1=self.xy3b,width= self.w_back_r)

        self.xy4b = [self.xy3b[0],self.xy1b[1]]
        return [*self.xy1b,*self.xyab,*self.xy2b,*self.xy3b,*self.xybb,*self.xy4b]        
    
    def roadleft(self):
        """ create section road left"""
        self.xy1l = [self.topleftpoint_p[0] - self.dis_r,
                self.topleftpoint_p[1]]
            
        self.xyal = cresectionpoint(point1=self.xy1l,width= self.w_left_r,direction="y_up")

        self.xy2l = [self.xy1l[0] - self.w_left_r,self.xy1l[1] ]

        self.xy3l = [self.xy2l[0], self.bottomrightpoint_p[1]]

        self.xybl = cresectionpoint(point1=self.xy3l,width= self.w_left_r,direction="y_bottom")        

        self.xy4l = [self.xy1l[0],self.xy3l[1]]

        return [*self.xy1l,*self.xyal,*self.xy2l,*self.xy3l,*self.xybl,*self.xy4l]

    def roadright(self):
        """ create section road right"""
        self.xy1r = [self.bottomrightpoint_p[0] + self.dis_r,
                self.bottomrightpoint_p[1]]

        self.xyar = cresectionpoint(point1=self.xy1r,
                            width= self.w_right_r,
                            direction="y_bottom")

        self.xy2r = [self.xy1r[0] + self.w_right_r,self.xy1r[1] ]

        self.xy3r = [self.xy2r[0], self.topleftpoint_p[1]]

        self.xybr = cresectionpoint(point1=self.xy3r,
                            width= self.w_right_r,
                            direction="y_up") 

        self.xy4r = [self.xy1r[0],self.xy3r[1]]

        return [*self.xy1r,*self.xyar,*self.xy2r,*self.xy3r,*self.xybr,*self.xy4r]

    def toprandbottoml_roadfront (self):
        """return top left and bottom right of road front"""
        return [self.xy1f,self.xy3f]
        
    def toprandbottoml_roadback (self):
        """return top left and bottom right of road back"""
        return [self.xy1b,self.xy3b]

    def toprandbottoml_roadleft (self):
        """return top left and bottom right of road left"""
        return [self.xy1l,self.xy3l]

    def toprandbottoml_roadright (self):
        """return top left and bottom right of road left"""
        return [self.xy1r,self.xy3r]

        

def cresectionpoint(point1, width = 100, direction = "y_left",hsh = 6, hsv = 8 ):

    if direction == "y_left":
        p_center = [point1[0],point1[1] + -(width/2)]
        p_t = [p_center[0],p_center[1] - width/hsv ]
        p_d =  [p_center[0],p_center[1] + width/hsv ]
        p_2 = [p_d[0] - width/hsh,p_d[1]]
        p_3 = [p_t[0] + width/hsh,p_t[1]]
        return [*p_d,*p_2,*p_3,*p_t]
    elif direction == "y_right":
        p_center = [point1[0],point1[1] + (width/2)]
        p_t = [p_center[0],p_center[1] - width/hsv ]
        p_d =  [p_center[0],p_center[1] + width/hsv ]
        p_2 = [p_t[0] + width/hsh,p_t[1]]
        p_3 = [p_d[0] - width/hsh,p_d[1]]
        return [*p_t,*p_2,*p_3,*p_d]
    
    elif direction == "y_up":
        p_center = [point1[0]- (width/2),point1[1]]
        p_t = [p_center[0]- width/hsv,p_center[1]]
        p_d =  [p_center[0] + width/hsv,p_center[1]]
        p_2 = [p_d[0] ,p_d[1]+ width/hsh]
        p_3 = [p_t[0] ,p_t[1]- width/hsh]
        return [*p_d,*p_2,*p_3,*p_t]

    elif direction == "y_bottom":
        p_center = [point1[0] + (width/2),point1[1]]
        p_t = [p_center[0]+ width/hsv,p_center[1]]
        p_d =  [p_center[0] - width/hsv,p_center[1]]
        p_2 = [p_d[0] ,p_d[1]+ width/hsh]
        p_3 = [p_t[0] ,p_t[1]- width/hsh]
        return [*p_d,*p_2,*p_3,*p_t]
        
        

    


    





    
    

    


    