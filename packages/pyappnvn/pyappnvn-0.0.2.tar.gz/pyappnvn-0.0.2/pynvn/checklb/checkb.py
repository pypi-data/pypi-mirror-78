import tkinter as tk
from pynvn.autoscrollbar.autoscrbar import AutoScrollbar

class ChecklistBox:
    """return check list box"""
    def __init__(self, parent, 
                choices = ["Nhuan", "Hong", "Trum","Nhuan", "Hong", "Trum"], 
                i = 1,
                onvalue = True,
                offvalue = "" ,
                width = 60,
                listsheetname = None,
                midstr = "_ Sheet name: ",
                texttitle = "File Name _ sheet Name",
                **kwargs):
        self.choices = choices
        self.onvalue = onvalue
        self.offvalue = offvalue
        self.parent = parent
        self.vars = []
        self.i = i
        self.width = width
        self.listsheetname = listsheetname
        self.midstr = midstr
        self.texttitle = texttitle
        self.__rechecklistbox()
    def __rechecklistbox (self):
        """ return check list box from arr """
        for idx,choice in enumerate(self.choices):
            var = tk.StringVar()

            self.vars.append(var)
            listname = "" if self.listsheetname == None else self.listsheetname[idx]
            if self.texttitle != "":
                lb = tk.Label (self.parent,text = self.texttitle,bg = "white")
                lb.grid(row=0,
                        column=0, 
                        sticky =  tk.W)
            cb = tk.Checkbutton(self.parent, 
                                var=var, 
                                text=choice + self.midstr + listname,
                                onvalue=choice,
                                offvalue=self.offvalue,
                                anchor=tk.W, 
                                bg = "azure",
                                relief="flat", 
                                highlightthickness=0
                                )
            cb.grid(row=self.i,
                        column=0,
                        sticky = tk.NSEW,
                        ) 
            self.i = self.i + 1

    def getCheckedItems(self):
        """ get checked items """
        return [var.get() for var in self.vars if var.get() !=""]