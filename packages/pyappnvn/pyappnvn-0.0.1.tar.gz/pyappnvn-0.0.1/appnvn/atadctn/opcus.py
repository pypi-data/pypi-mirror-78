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

from pynvn.cavaszm.cavaszm import zmcv

from pynvn.nsew.nsew import directnmwe

from pynvn.cavas_write.writetext import writetext

from pynvn.cavas_drawing.draw import dcavas
import string
class opcus(tk.Frame):
        """Customer information"""
        def __init__(self,tktk = None,
                        canvasb = None,
                        controller= None,
                        bglb = "white",
                        labelfont = ('times', 20),
                        labelfont_sm = ('times', 16),
                        imagenext = None,
                        imagepre = None,
                        frameb = [450,0,750,750,"aquamarine2"],
                        cavheight_width = [1200,750],
                        w_front = 100,
                        imagenextlayout = None,
                        imageprelayout = None,
                        dirfolder = None,
                        *args,**kwargs):
                tk.Frame.__init__(self, tktk, bg = "azure")
                self.controller = controller
                self.labelfont = labelfont
                self.labelfont_sm = labelfont_sm
                self.bglb = bglb
                self.imagenext = imagenext
                self.imagepre = imagepre
                self.height = kwargs["height"]
                self.width = kwargs["width"]
                self.dirfolder = dirfolder
                # set back area
                self.w_front =  w_front
                self.w_back =  kwargs["w_back"]
                self.w_left =  kwargs["w_left"]
                self.w_right =  kwargs["w_right"]
                # traffice around
                self.wr_front =  kwargs["wr_front"]
                self.wr_back =  kwargs["wr_back"]
                self.wr_left=  kwargs["wr_left"]
                self.wr_right= kwargs["wr_right"]
                self.dis_r = kwargs["dis_r"]
                self.dis_dim = self.dis_r/3
                self.dis_direc = kwargs["dis_direc"]
                self.frameb = frameb 
                self.imagenextlayout = imagenextlayout

                self.sc = scbg(parent = self,
                                cavheight=self.frameb[3] ,
                                cavwidth=self.frameb[2] ,
                                bg = self.frameb[4], 
                                isonlyaframe= True,
                                frameincavas= True,
                                bgpr= self.frameb[4],
                                )
                # return cavas 
                framecv = self.sc.framecv
                self.canvasb =self.sc.canvas
                #self.createdrawing()
                self.pattern = re.compile("[0-9]")
                self.createdrawing()
                # scale,zoom,move in cavas 
                zmcv(cavas=self.canvasb,
                                frameb=self.frameb,
                                value_dis=self.value_dis,
                                centerp =self.centerp, 
                                usingcoord = True)
                
        def createdrawing (self, colorroad = "#c49b65",*args,**kwargs):
                """Drawing layout follow customer"""
                plc = placereccenter(info_height_k= self.height,
                                        info_width_k= self.width,
                                        info_width_P =self.frameb[2],
                                        info_height_p=self.frameb[3]
                                        )
                self.centerp = plc.pointcenterofparent()
                # top left
                self.leftpoint = plc.pointleftrec()

                # top right
                self.rightpoint = plc.pointrightrec()

                # create rectangle parent
                dcavas (cavas=self.canvasb,
                                topp=self.leftpoint,
                                bottomp =self.rightpoint \
                                ).drec(fill="yellow")
                #set back road  
                plcn = setbackdimention(w_front=self.w_front,
                                        w_back=self.w_back,
                                        w_left=self.w_left,
                                        w_right=self.w_right,
                                        topleftpoint_p=self.leftpoint,
                                        bottomrightpoint_p=self.rightpoint 
                                        )
                                        
                self.topleftkid = plcn.topleftpoint()
                self.toprightkid = plcn.toprightpoint()
                # create rectangle kid
                dcavas (cavas=self.canvasb,
                        topp=self.topleftkid,
                        bottomp =self.toprightkid)\
                        .drec(fill="#e79c2b")
                # create road for front 
                rf = create_poly_from_tleft_bright(topleftpoint_p=self.leftpoint,
                                                        bottomrightpoint_p=self.rightpoint,
                                                        w_front_r= self.wr_front,
                                                        w_back_r=self.wr_back,
                                                        w_left_r=self.wr_left,
                                                        w_right_r=self.wr_right,
                                                        dis_r=self.dis_r
                                                )
                rfa = rf.roadfront()
                #create front of road
                self.createfront(rfa,fill = colorroad)
                tlrf = rf.toprandbottoml_roadfront()
                # create road for back 
                rba  =rf.roadback()
                self.createback(rba,fill = colorroad)
                # create top left and bottom  back of road 
                tlrb = rf.toprandbottoml_roadback()
                # create road for left
                rbl  =rf.roadleft()
                self.createleft(rbl,fill = colorroad)
                tlrl = rf.toprandbottoml_roadleft()
                # create road for right
                rbr  =rf.roadright()
                self.createright(rbr,fill = colorroad)
                tlrr = rf.toprandbottoml_roadright()
                # dim for item all
                self.coord = coordp(topleftp=self.leftpoint,
                                bottomrightp=self.rightpoint,
                                rev_direction="left",
                                topleftk=self.topleftkid,
                                bottomrightk=self.toprightkid,
                                dis_dim=self.dis_dim)
                # create dim for h 
                self.dimforh()
                #dim for top
                self.dimforw()
                #dim for setback front
                self.dimforsbf()
                #dim for setback back 
                self.dimforsbb()
                #dim for setback left 
                self.dimforsbl()
                #dim for setback right 
                self.dimforsbr()
                # dim for road front
                self.dimforroadfront(tlrf=tlrf)
                # dim for road back
                self.dimforroadback (tlrb=tlrb)
                # dim for road left
                self.dimforroadleft(tlrl=tlrl)
                # dim for road right
                self.dimforroadright(tlrr=tlrr)
                #caculate for area 
                writetext(canvas=self.canvasb,
                                topleftkid=self.topleftkid,
                                toprightkid= self.toprightkid,
                                centerpoint = self.coord.centerpointkid()).warea()
                                
                # create direction nwse
                nsew = directnmwe(canvasb = self.canvasb,
                                height = self.height, 
                                width = self.width,
                                dis_r = self.dis_r,
                                wr_front = self.wr_front,
                                wr_back = self.wr_back,
                                wr_left = self.wr_left,
                                wr_right = self.wr_right,
                                dis_direc = self.dis_direc, 
                                leftpoint= self.leftpoint, 
                                rightpoint=self.rightpoint
                                )
                nsew.nsew(font = ('times', 16),fill = "black")
                self.value_dis = nsew.revalue_dis()

        def createrectang_area(self,topleftpoint = None, 
                                toprightpoint = None, 
                                fill = "yellow",
                                alpha=0.5 ):

                """ create rectangle of area """
                self.rrectangle_wd = self.canvasb.create_rectangle (*topleftpoint,
                                                                        *toprightpoint,
                                                                        fill=fill)
        def reratio (self):
                """ caculate ratio of window"""
                try:
                        self.minradio = ratio(real_w=self.frameb[2],
                                        real_h=self.frameb[3],
                                        w = self.value_dis * 2 ,
                                        h =self.value_dis * 2).reratiomin()
                except:
                        messagebox.showerror("Eror", "check ratio of class ratio" )

        def currentsize (self):
                """ Current size to setup when event"""
                self.reratio()
                self.canvasb.scale("all",
                                self.frameb[2]/2, 
                                self.frameb[3]/2, 
                                self.minradio/1.1, 
                                self.minradio/1.1)

        def createrecp (self):
                """Create rectangle of widget parent"""
                try:

                        self.canvasb.delete(self.rectangle_wd ) # remove
                except:
                        pass
                # create rectange of parent 
                self.rectangle_wd = self.canvasb.create_rectangle (*self.leftpoint,
                                                                        *self.rightpoint,
                                                                        fill="red"
                                                                        )
        def createreck (self,**kwargs):
                """Create rectangle of widget kid"""
                try:

                        self.canvasb.delete(self.rrectangle_kid ) # remove
                except:

                        pass

                self.rrectangle_kid = self.canvasb.create_rectangle (*self.topleftkid,
                                                                        *self.toprightkid,
                                                                        fill="#e79c2b"
                                                                        )
        
        def createfront(self,rfa,**kwargs):
                """Create front road"""
                if  int(self.wr_front) != 0:
                        try:

                                self.canvasb.delete(self.crrf ) # remove
                        except:
                                pass                

                        self.crrf = self.canvasb.create_polygon(*rfa,**kwargs)

        def createback(self,rfa,**kwargs):
                """create back road"""
                if  int(self.wr_back) != 0:
                        try:

                                self.canvasb.delete(self.ra ) # remove
                        except:
                                pass                

                        self.ra = self.canvasb.create_polygon(*rfa,**kwargs)

        def createleft(self,rfa,**kwargs):
                """create left road"""
                if  int(self.wr_left) != 0:
                        try:

                                self.canvasb.delete(self.rf ) # remove
                        except:
                                pass                

                        self.rf = self.canvasb.create_polygon(*rfa,**kwargs)

        def createright(self,rfa,**kwargs):
                """create right road"""
                if  int(self.wr_right) != 0:
                        try:
                                self.canvasb.delete(self.rr ) # remove
                        except:
                                pass                

                        self.rr = self.canvasb.create_polygon(*rfa,**kwargs)
        
        def dimforh(self,**kwargs):
                try:

                        self.canvasb.delete(self.rll ) # remove
                except:
                        pass

                coordse = self.coord.pointstartend()

                self.rll = self.canvasb.create_line(*coordse,
                                                        fill = "red",
                                                        arrow = "both")
                # create text 

                try:

                        self.canvasb.delete(self.cvt ) # remove
                except:
                        pass

                coordtext =self.coord.centertowpoint()

                self.cvt = self.canvasb.create_text(*coordtext, 
                                                        anchor="n",
                                                        text =str(self.height), 
                                                        angle=90)
        def dimforw(self,**kwargs):
                try:
                        self.canvasb.delete(self.dfwl ) # remove
                except:
                        pass
                self.coord.rev_direction = "top"
                coordse = self.coord.pointstartend()

                self.dfwl = self.canvasb.create_line(*coordse,
                                                        fill = "red",
                                                        arrow = "both"
                                                        )
                # create text 
                try:

                        self.canvasb.delete(self.dfwt ) # remove
                except:
                        pass
                coordtext =self.coord.centertowpoint()

                self.dfwt = self.canvasb.create_text(*coordtext, 
                                                        anchor="n",
                                                        text =str(self.width), 
                                                        angle=0)

        def dimforsbf (self,**kwargs):
                
                try:
                        self.canvasb.delete(self.dfsbfl ) # remove
                except:
                        pass
                self.coord.dis_dim = self.width/2
                dfsbfl = self.coord.fronttowpoint()
                #coordse = coord.pointstartend()

                self.dfsbfl = self.canvasb.create_line(*dfsbfl,
                                                        fill = "red",
                                                        arrow = "both"
                                                        )
                
                # create text 
                try:

                        self.canvasb.delete(self.dfsbft ) # remove
                except:
                        pass
                coordf =self.coord.fronttowpointcenter()
                if  int(self.w_front) != 0 :
                        self.dfsbft = self.canvasb.create_text(*coordf, 
                                                                anchor="s",
                                                                text =str(self.w_front), 
                                                                angle=90)      
        
        def dimforsbb (self,**kwargs):
                
                try:

                        self.canvasb.delete(self.dfsbbl) # remove
                except:
                        pass
                sbb = self.coord.backtowpoint()

                self.dfsbbl = self.canvasb.create_line(*sbb,
                                                        fill = "red",
                                                        arrow = "both"
                                                        )
                
                # create text 
                try:

                        self.canvasb.delete(self.dfsbbt ) # remove
                except:
                        pass
                coordf =self.coord.backtowpointcenter()

                if  int(self.w_back) != 0 :

                        self.dfsbbt = self.canvasb.create_text(*coordf, 
                                                                anchor="s",
                                                                text =str(self.w_back), 
                                                                angle=90)

        def dimforsbl(self,**kwargs):

                try:
                        self.canvasb.delete(self.dfsbl ) # remove
                except:
                        pass
                self.coord.dis_dim = self.height / 2
                sbl = self.coord.lefttowpoint()

                self.dfsbl = self.canvasb.create_line(*sbl,
                                                        fill = "red",
                                                        arrow = "both"
                                                        )

                # create text 
                try:
                        self.canvasb.delete(self.dfsbt ) # remove
                except:
                        pass
        
                coordl =self.coord.lefttowpointcenter()

                if  int(self.w_left) != 0 :

                        self.dfsbt = self.canvasb.create_text(*coordl, 
                                                                anchor="s",
                                                                text =str(self.w_left), 
                                                                angle=0)
        
        def dimforsbr(self,**kwargs):

                try:
                        self.canvasb.delete(self.dfsbrl ) # remove
                except:
                        pass
                sbr = self.coord.righttowpoint()
                #coordse = coord.pointstartend()

                self.dfsbrl = self.canvasb.create_line(*sbr,
                                                        fill = "red",
                                                        arrow = "both"
                                                        )
                
                # create text 
                try:

                        self.canvasb.delete(self.dfsbrt ) # remove
                except:
                        pass
                coordr =self.coord.righttowpointcenter()

                if  int(self.w_right) != 0 :

                        self.dfsbrt = self.canvasb.create_text(*coordr, 
                                                                anchor="s",
                                                                text =str(self.w_right), 
                                                                angle=0)

        def dimforroadfront(self,tlrf,**kwargs):

                if  int(self.wr_front) != 0 :
                        coordf = coordp(topleftp=tlrf[0],
                                        bottomrightp=tlrf[1],
                                        rev_direction="left",
                                        dis_dim =30)
                        try:

                                self.canvasb.delete(self.dfrf ) # remove
                        except:
                                pass
                        coordf.dis_dim = - self.width / 2
                        coordse = coordf.pointstartend()

                        self.dfrf = self.canvasb.create_line(*coordse,
                                                                fill = "red",
                                                                arrow = "both")

                        # create text 
                        try:

                                self.canvasb.delete(self.tfrf ) # remove
                        except:
                                pass
                        coordtext =coordf.centertowpoint()

                        self.tfrf = self.canvasb.create_text(*coordtext, 
                                                                anchor="n",
                                                                text =str(self.wr_front), 
                                                                angle=90)
        
        def dimforroadback(self,tlrb,**kwargs):
                """ dim for road back """
                if  int(self.wr_back) != 0 :
                        coordf = coordp(topleftp=tlrb[0],
                                        bottomrightp=tlrb[1],
                                        rev_direction="left",
                                        dis_dim=30)
                        try:

                                self.canvasb.delete(self.dfrb ) # remove
                        except:
                                pass
                        coordf.dis_dim =  self.width / 2
                        coordse = coordf.pointstartend()
                

                        self.dfrb = self.canvasb.create_line(*coordse,
                                                                fill = "red",
                                                                arrow = "both")

                        # create text 
                        try:

                                self.canvasb.delete(self.tfrb ) # remove
                        except:
                                pass
                        coordtext =coordf.centertowpoint()

                        self.tfrb = self.canvasb.create_text(*coordtext, 
                                                                anchor="n",
                                                                text =str(self.wr_back), 
                                                                angle=90)

        def dimforroadleft(self,tlrl,**kwargs):
                """ dim for road left """
                if  int(self.wr_left) != 0 :
                        coordf = coordp(topleftp=tlrl[0],
                                        bottomrightp=tlrl[1],
                                        rev_direction="top",
                                        dis_dim=30)
                        try:

                                self.canvasb.delete(self.dfrl ) # remove
                        except:
                                pass
                        coordf.dis_dim = - self.height / 2
                        coordse = coordf.pointstartend()
                

                        self.dfrl = self.canvasb.create_line(*coordse,
                                                                fill = "red",
                                                                arrow = "both")

                        # create text 
                        try:

                                self.canvasb.delete(self.tfrl ) # remove
                        except:
                                pass
                        coordtext =coordf.centertowpoint()

                        self.tfrl = self.canvasb.create_text(*coordtext, 
                                                                anchor="n",
                                                                text =str(self.wr_left), 
                                                                angle=0)

        def dimforroadright(self,tlrr,**kwargs):
                """ dim for road right """
                if  int(self.wr_right) != 0 :
                        coordf = coordp(topleftp=tlrr[0],
                                        bottomrightp=tlrr[1],
                                        rev_direction="top",
                                        dis_dim=30)
                        try:

                                self.canvasb.delete(self.dfrr ) # remove
                        except:
                                pass
                        coordf.dis_dim = self.height / 2
                        coordse = coordf.pointstartend()
                

                        self.dfrr = self.canvasb.create_line(*coordse,
                                                                fill = "red",
                                                                arrow = "both")
                        # create text 
                        try:

                                self.canvasb.delete(self.tfrr ) # remove
                        except:
                                pass
                        coordtext = coordf.centertowpoint()

                        self.tfrr = self.canvasb.create_text(*coordtext, 
                                                                anchor="n",
                                                                text =str(self.wr_right), 
                                                                angle=0)
