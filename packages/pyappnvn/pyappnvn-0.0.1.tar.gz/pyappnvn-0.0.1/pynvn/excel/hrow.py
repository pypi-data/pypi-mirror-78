from pynvn.excel.list import lnumbercolumnbyrangstr
from pynvn.string.slist import returnseplistintbbystr
from pynvn.excel.rows import startrow_endrow
class hrow(object):
    """ 
    handling range for sheet\n
    rmrange: Range to handling string: \n
    ex: A1, A1:B3,A
    ws: worksheet corresponds to the rmrange \n
    option: style to  handling:\n
    ex: tspacetoospace, fs,upper_all,both, left, right,lower_all,all \n
    option_fun: For case function "REMOVESPACE or CAPFS" user select from interface \n
    ex: REMOVESPACE,CAPFS
    """
    def __init__(self,f):
        self.f = f
    def __call__(self,*args, **kwargs):
        ws = kwargs["ws"]
        rmrange = kwargs["rmrange"]
        using_value_to_end = kwargs.get("using_value_to_end",True)
        value_to_end = kwargs.get("value_to_end","End")
        valuetodelete = kwargs.get("valuetodelete",["",None])
        for rangea in rmrange:
            cols=lnumbercolumnbyrangstr(rstr=rangea)
            rows=returnseplistintbbystr(strint=rangea)
            a,b = startrow_endrow(ws=ws,
                                rows=rows,
                                cols=cols
                                )
            for col in cols:
                self.f(index_col=col,
                        ws=ws,
                        startrow=a,
                        endrow=b,
                        using_value_to_end= True,
                        valuetodelete=["",None],
                        value_to_end="VTC"
                        )
                        