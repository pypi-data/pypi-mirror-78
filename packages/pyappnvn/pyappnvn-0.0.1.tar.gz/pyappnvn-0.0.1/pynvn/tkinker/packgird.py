def forget(widget): 
    """ invisible gird and pack """
    # This will remove the widget from toplevel 
    #basically widget do not get deleted 
    # it just becomes invisible and loses its position 
    # and can be retrieve 
    widget.grid_forget()        
def return_gird_pack(widget,
                    insidepackorgird = "gird",
                    **kw):
    """ visible gird and pack """
    widget.grid(**kw) if insidepackorgird == "gird" else widget.pack(**kw)

