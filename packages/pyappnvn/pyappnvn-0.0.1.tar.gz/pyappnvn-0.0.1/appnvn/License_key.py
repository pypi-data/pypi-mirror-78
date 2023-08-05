from appnvn.atadctn.icontt import gui
from pynvn.authkey import authkey
from pynvn.crypt import (write_key,
                        load_key,
                        encrypt,
                        decrypt
                        )
from pynvn.mc_id import mcwd_id
import tkinter as tk  

class key_license:
    """ 
    license key of app
    check valid key (valid or invalid)
    """
    def __init__(self,tktk = None,
                    pathtokey = None,
                    pathtovaluecsv_key = None,
                    ser_key = None,
                    valueser_key = None,
                    product_id = 7018,
                    using_permanent_key = False,
                    path_mc_id = None,
                    **kw):
        self.__tktk = tktk
        self.result = False
        key = load_key(ser_key)
        
        try:
            valueser_key_de = decrypt(filename=valueser_key,
                                    key = key)
        except:
            valueser_key_de = None

        aucre = authkey(
                    product_id=product_id,
                    key=valueser_key_de,
                    pathtokey = pathtokey,
                    pathtovaluecsv_key = pathtovaluecsv_key,
                    using_permanent_key = using_permanent_key,
                    path_mc_id = path_mc_id,
                    valueser_key = valueser_key,
                    ser_key = ser_key
                    )
        if aucre[0] == False:
            guiforinser(tktk=tktk,
                pathtokey =pathtokey,
                pathtovaluecsv_key= pathtovaluecsv_key,
                ser_key = ser_key,
                valueser_key = valueser_key,
                using_permanent_key = using_permanent_key,
                product_id = product_id,
                path_mc_id = path_mc_id,
                **kw
                )
        else:
            self.result = True
    
class guiforinser:
    """
    class gui input for key 
    """
    def __init__(self,tktk = None,
                    pathtokey = None,
                    pathtovaluecsv_key = None,
                    valueser_key = None,
                    ser_key = None,
                    product_id = None,
                    using_permanent_key = False,
                    path_mc_id  = None,
                    **kw
                ):
        
        self.__tktk =  tktk

        tktk['bg']="#5b9bd5"
        
        self.pathtokey = pathtokey
        self.pathtovaluecsv_key = pathtovaluecsv_key
        self.valueser_key = valueser_key
        self.ser_key = ser_key
        self.product_id = product_id
        self.using_permanent_key = using_permanent_key
        self.path_mc_id = path_mc_id
        gui (tktk=tktk,**kw).setcfbs()
        self.gui_ser()

    def gui_ser(self):
        
        in_info = tk.Label(self.__tktk, 
                            text ="Input your key below:",
                            font="Times 20 italic bold",
                            bg =  "#5b9bd5"
                            )
        in_info.place(relx = 0.5,
                    rely = 0.2,
                    anchor= tk.CENTER)


        self.can_en = tk.Entry (self.__tktk ,
                        width = 35,
                        justify = tk.CENTER,
                        font="Times 15 italic"
                        ) 
        self.can_en.place(relx = 0.5,
                            rely = 0.35,
                            anchor= tk.CENTER)

        button_key = tk.Button(text='OK', 
                            command=lambda: self._valid_key(),
                            font="Times 12 italic",
                        )
        button_key.place(relx = 0.5,
                            rely = 0.5,
                            anchor= tk.CENTER)

    def _valid_key (self):
        """ check valid key """
        x1 = self.can_en.get()
        key = load_key(self.ser_key)
        try:
            if decrypt(filename = self.valueser_key,key=key) == x1:
                encrypt(filename=self.path_mc_id,
                    key = key,
                    nametow=mcwd_id().encode('utf_8'))
        except:
            pass
        aucre  = authkey(
                    product_id=self.product_id,
                    key=str(x1),
                    pathtokey = self.pathtokey,
                    pathtovaluecsv_key = self.pathtovaluecsv_key,
                    path_mc_id = self.path_mc_id,
                    valueser_key = self.valueser_key,
                    using_permanent_key=self.using_permanent_key,
                    ser_key=self.ser_key
                    )
        label1 = tk.Label(self.__tktk, 
                    text= "the key is invalid or it can not be activated",
                    fg="red")

        if aucre[0] == False:
            label1.place(relx = 0.5,
                            rely = 0.65,
                            anchor= tk.CENTER)
        else:
            write_key(self.ser_key)
            key = load_key(self.ser_key)
            encrypt(filename=self.valueser_key,
                key = key,
                nametow=str(x1).encode('utf_8'))

            encrypt(filename=self.path_mc_id,
                key = key,
                nametow=mcwd_id().encode('utf_8'))
        
            tk.messagebox.showinfo("Activation Wizard",
                                    "Activation successful, License expires: " + aucre[1] )
            self.__tktk.quit()