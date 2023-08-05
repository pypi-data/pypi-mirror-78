from pynvn.excel import closeallfileexcel
class valueerror(Exception):
    def __init__(self, value):
        messagebox.showerror("Error",value)
