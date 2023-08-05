import itertools
""" 
class to handing data with symbol special 
import itertools
"""
class hstring:
    def  __init__(self, stringtohl = None,
                 igchar = None, 
                 path_cof = None,
                 chartorepign = None
                                        ):
        # ignore character     
        self.igchar = igchar 
        # path to conf
        self.path_cof = path_cof
        # string to handling 
        self.stringtohl = stringtohl
        #char to replace ignore character 
        self.chartorepign = chartorepign

    #string to remove char 
    def stringremoveigcharreturnspace(self):
        return self.stringtohl.translate({ord(i):self.chartorepign
                                             for i in self.igchar})

    #remove fist and end char 
    def revdupconstrfirstend(self):
        # check and replace fist string
        stfirst = self.replacecharinstrbyindex(0) if self.stringtohl[0]\
                                     in self.igchar  else self.stringtohl

        #set new parameter for stringtohl
        self.stringtohl = stfirst
        # check and replace end string
        stsecond = self.replacecharinstrbyindex(-1) if self.stringtohl[-1]\
                                 in self.igchar  else self.stringtohl
        return stsecond

    #replace char in by index from string, return string 
    def replacecharinstrbyindex (self, index):
        # convert string to list 
        tringh = list(self.stringtohl)
        #replace value index to chart replace 
        tringh[index] = self.chartorepign
        #convert to string
        st = "".join(tringh)
        return st

    # to remove continue return only single character , return string
    def removecontireturnsingle(self):
        tringh = list(self.stringtohl)
        i = 0 
        while i < len(tringh) - 1:
            if (tringh[i] in self.igchar and (tringh[i] == tringh[i+1])):
                del  tringh[i]
            else:
                i = i + 1
        st = "".join(tringh)
        return st

# return back to processed data, return string

"""
    stringtohl: string to handling 
    igchar : ignore character 
    chartorepign " character to replace 
"""
def returnvaluelist (stringtohl,
                        igchar,
                        chartorepign):
    

   hstring_hl =  hstring(stringtohl = stringtohl,
                                    igchar = igchar,
                                    chartorepign = chartorepign)

   hstring_hled = hstring_hl.stringremoveigcharreturnspace()
   # set new value for class
   hstring_hl.stringtohl = hstring_hled
   # set char to replace 
   hstring_hl.chartorepign = ""
   # remove char fist and end 
   hstring_hl1 = hstring_hl.revdupconstrfirstend()

   hstring_hl.stringtohl = hstring_hl1
   # set char to replace 
   hstring_hl.chartorepign = ","

   hstring_hl2 = hstring_hl.removecontireturnsingle()
   #python code to convert string to list 
   hstringlist = list(hstring_hl2.split(","))

   return hstringlist
#retl = returnvaluelist("(21:9),(21:11),(20:10),(22:10)",",.(:)",",")
#print ("retl",retl)

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)
def duprowdata(df):
    for cols in df.columns:
        try:
            value = df.loc[1, cols]
            if value == None:
                value = ""       
        except:
            pass
        df[cols].fillna(value,inplace = True) 
    return df