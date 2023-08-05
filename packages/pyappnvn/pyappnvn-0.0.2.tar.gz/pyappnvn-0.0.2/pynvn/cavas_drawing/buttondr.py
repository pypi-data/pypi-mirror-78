import tkinter as tk
def crebutton (cavas,crwidth = 180 ,crheight = 480,namebutton ="FIND",*args,**kwargs):
        button1 = tk.Button(cavas, 
                      text = namebutton,
                      anchor = tk.CENTER,
                      **kwargs,
                      )
        button1_window = cavas.create_window(crwidth, crheight, 
                                              anchor=tk.CENTER, 
                                              window=button1)
