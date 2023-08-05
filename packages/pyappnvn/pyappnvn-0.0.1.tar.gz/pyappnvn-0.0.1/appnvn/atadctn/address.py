import tkinter as tk
from tkinter import ttk
def address(listFramevp,row  = 3):
    #set Address
    row = row + 1
    add = tk.Label(listFramevp,
                                text = "*Address:"
                                )
    add.grid(column = 0, 
                        row  = row ,
                        sticky  = "w",
                        )

    # set Province or city
    pc = tk.StringVar() 
    combopc =  ttk.Combobox(listFramevp, textvariable = pc)
    combopc['values'] = ('Province/City',  
                                ' Dak Lak', 
                                ' Ho Chi Minh', 
                                ' Ha Noi', 
                                ' Dong Nai', 
                                ' Long An'
                                )

    combopc.current(0)
    combopc.grid(column = 1, row = row,columnspan = 4,sticky  = tk.EW) 
    # set District or Town
    dt = tk.StringVar() 
    combodt =  ttk.Combobox(listFramevp, textvariable = dt)
    combodt['values'] = ('District/Town',  
                                'Krong Buk', 
                                'Buon Ho', 
                                'Ehleo', 
                                '1 District', 
                                '2 District', 
                                '3 District', 
                                '4 District'
                                ) 
    combodt.current(0)
    row = row + 1
    combodt.grid(column = 1, row = row, pady = 10,columnspan = 4,sticky  = tk.EW) 

    # set Ward/Village
    wv = tk.StringVar() 
    combowv =  ttk.Combobox(listFramevp, 
                                        textvariable = wv,style = 'custom.TCombobox')
    combowv['values'] = ('Ward/Village',  
                                ' Cu pong', 
                                ' Chu Kpo'
                                ) 
    combowv.current(0)
    row +=1
    combowv.grid(column = 1, row = row,columnspan = 4,sticky  = tk.EW) 

    v = StringVar(listFramevp, value='Address Street')
    adde = tk.Entry(listFramevp,
                                justify="left",
                                text = v
                                )
    adde.bind("<Button-1>", some_callback(adde))
    row +=1
    adde.grid(column = 1, 
                        row  = row,
                        sticky  = tk.EW,
                        pady = 10,
                        columnspan = 4
                        )
"""delete value defaut entry """
def some_callback(adde,event): # note that you must include the event as an arg, even if you don't use it.
                adde.delete(0, "end")
                return None