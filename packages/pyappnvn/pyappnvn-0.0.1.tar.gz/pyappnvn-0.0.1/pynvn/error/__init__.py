from tkinter import messagebox
def mssage_error(cont1,cont2,title = "Error"):
    messagebox.showerror("title","check again parameter {0} {1}".format(str(cont1).upper(),str(cont2).upper()))