import tkinter as tk # python 3
from appnvn.atadctn.treectn import scbg
from appnvn.atadctn.icontt import gui
from appnvn.atadctn.treectn import scrollbarvn
from pynvn.checklb.checkb import ChecklistBox
from pynvn.path.ppath import (listfileinfolder,
                                repathfolderchild
                                )
from pynvn.folder import remove_folder

class mlayout(tk.Tk):
    """ config layout, add layout more from input user """
    def __init__(self, 
                    tktk = None,
                    pathicon =None,
                    labelfont = ('times', 20),
                    labelfont_sm = ('times', 16),
                    labelfont_botton = ('times', 11), 
                    pathclayout = None,
                    *args,
                    **kwargs):

        self.__tktk = tktk
        self.__labelfont = labelfont
        self.__labelfont_sm = labelfont_sm
        self.__pathclayout = pathclayout
        self.__labelfont_botton = labelfont_botton
        self.__filewin = tk.Toplevel(self.__tktk)
        gui (tktk=self.__filewin,
            pathico=pathicon,
            width=800,
            height=800,
            widthx="center",
            widthy="center",
            resizable=[True,True],
            condv=2.7
            ).setcfbs()
        
        self.fa = [0,0,600,50,"white"]
        self.fb =  [0,50,600,150,"azure"]
        self.fc =  [0,200,600,150,"white"]

        self.sc  = scbg(parent = self.__filewin,
                        cavheight=600,
                        cavwidth=600,
                        isonlyaframe= False,
                        bg = "white",
                        bgpr = "#5b9bd5",
                        framea = self.fa,
                        frameb = self.fb,
                        framec = self.fc
                        )
        self.framea = self.sc.framea
        self.frameb = self.sc.frameb
        self.framec = self.sc.framec
        try: 
            self.scf.destroy()
        except:
            pass
        self.scf = scrollbarvn(parent=self.frameb,
                                bg = self.fb[4])

        self.scframe = self.scf.frame
        # return list file in folder
        lif = listfileinfolder(pathclayout)
        self.cb = ChecklistBox(parent=self.scframe,
                                choices=lif,
                                width= 159,
                                midstr="",
                                texttitle=""
                                )
        self.__creategui()
    def __creategui(self):
        """ create to input size layout """
        sltt = tk.Label(self.framea,
                        anchor = tk.CENTER,
                        text = "All layout of Container House",
                        font=self.__labelfont,
                        bg = self.fa[4],
                        )
        sltt.place(relx=0.5, rely=0.5, anchor="center")

        button1 = tk.Button(self.framec,
                            font=self.__labelfont_botton,
                            bd = 1,
                            text = "Delete",
                            command = lambda: self.__deletefolder()
                            )

        button1.grid(row = 0,
                    column = 0,
                    sticky = "e"
                    )

        button1 = tk.Button(self.framec,
                            font=self.__labelfont_botton,
                            bd = 1,
                            text = "Modify",
                            command = lambda: self.__deletefolder()
                            )
            
        button1.grid(row = 0,
                    column = 1,
                    sticky = "w"
                    )

        button1 = tk.Button(self.framec,
                            font=self.__labelfont_botton,
                            bd = 1,
                            text = "Exit",
                            command = lambda: self.__filewin.quit()
                            )

        button1.grid(row = 0,
                    column = 2,
                    sticky = "w"
                    )

    def __deletefolder (self):
        """ delete folder in layout"""
        listchecked = self.cb.getCheckedItems()
        for elel in listchecked:
            remove_folder(repathfolderchild(dirpath=self.__pathclayout,
                                            subFolder=elel,
                                            createfolderifnotexsting= False
                                            )
                                            )

        lif = listfileinfolder(self.__pathclayout)

        try: 
            self.scf.destroy()
        except:
            pass
        self.scf = scrollbarvn(parent=self.frameb, bg = self.fb[4])

        self.scframe = self.scf.frame

        self.cb = ChecklistBox(parent=self.scframe,
                                choices=lif,
                                width= 123,
                                midstr="",
                                texttitle=""
                                )