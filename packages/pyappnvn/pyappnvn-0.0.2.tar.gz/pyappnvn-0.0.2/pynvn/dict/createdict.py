from openpyxl.styles import Alignment

from pynvn.path import ReturnDataAllRowByIndexpath,returndatalistrowbyindex

class credict():
    def __init__(self,KeyValues = None,LocConf = None,
                 Config_Setting_Path = None):
        self.Config_Setting_Path = Config_Setting_Path
        self.KeyValues = KeyValues
        self.LocConf = LocConf

    # create dict from key and value 
    def dictfromkeyandvalue(self):
        return dict (zip(self.KeyValues,
                    self.LocConf))

    # get value from conf path 
    def getvaluefromconfigpath(self):
        #list of value 
        valuelist = [[(i) for i in returndatalistrowbyindex(self.Config_Setting_Path,k)] for k in self.LocConf]
        #set new value list 
        return valuelist

    # create dicr from key and config setting path 
    def Dictfromkeyandvalueconf(self):
        valuelist = self.getvaluefromconfigpath()
        return dict (zip(self.KeyValues,
                    valuelist))

# update lists together 
def updictjoint(*List):
    Genenral_Dict = {} 
    for subDict in List:
        Genenral_Dict.update(subDict)
        gendictsorted = (sorted (Genenral_Dict.items()))
        gendictsorted = dict(gendictsorted)
    return gendictsorted

    
    
""""
         keyvalue = [ValueGeneral,
                Columnmove,
                LocationCellForMoveColumn,
                GenneralColumnNotChange,
                GeneralConcernRaffter,
                Genneral_Select,
                LocationOfRowLeft,
                LocationOfRowRight,
                ExcelCellForMoveColumnRight,
                LocationOfPurlin]

[12,16,17,19,20,21,23,24,25,26]



ValueGeneral = [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,12)]
#remove Column move 
#Columnmove = ReturnDataAllRowByIndexpath(Config_Setting_Path,32)
Columnmove = [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,16)]

LocationCellForMoveColumn = ReturnDataAllRowByIndexpath(Config_Setting_Path,17)

ArrRangMax = [* range(max([int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,11)] + Columnmove + [int(i) for i in  ReturnDataAllRowByIndexpath(Config_Setting_Path,0)]) + 1)]

ValueChangeLeft_Right  = set(ArrRangMax).difference(set(ValueGeneral + Columnmove))

IndexChangeRemoveColumn = set([int(i) for i in  ReturnDataAllRowByIndexpath(Config_Setting_Path,0)]).difference(set(Columnmove))

GenneralColumnNotChange =  [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,19)]

GeneralConcernRaffter = [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,20)]

Genneral_Select = [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,21)]

LocationOfRowLeft = [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,23)]

LocationOfRowRight = [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,24)]

ExcelCellForMoveColumnRight = ReturnDataAllRowByIndexpath(Config_Setting_Path,25)

LocationOfPurlin =  [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,26)]

TitleLocationMoveColumn = ReturnDataAllRowByIndexpath(Config_Setting_Path,27)

Index_Path_From_CSV  = ReturnDataAllRowByIndexpath(Config_Setting_Path,28)

startrow = ReturnDataAllRowByIndexpath(Config_Setting_Path,30)

"""
"""
class StringProcessing:
    def  __init__(self, path = None):
        self.path = path
        self.Return_Arr_Re = PathSteel(self.path)
        self.Arr_characters_special = self.Return_Arr_Re.ReturnDataAllRowByIndexpath(1)
        self.KeepValueNotChange = self.Return_Arr_Re.ReturnDataAllRowByIndexpath(0) 
        self.ArrReturn = self.Return_Arr_Re.ReturnDataAllRowByIndexpathAll()
        self.Check_Con_To_Case_Expect = self.Return_Arr_Re.ReturnDataAllRowByIndexpath(2)
        self.keys = self.ArrReturn[3]
    def Handling_Data_Tr (self,Arr_Index_Element,Arr):
        Arr_Index_Element = list(func(Arr_Index_Element))
        Arr_Element = [Arr[(vt[0]+1):(vt[1])] for vt in Arr_Index_Element]
        Arr_Element_El = Remove(Arr_Element)
        if "" in Arr_Element_El:
            Arr_Element_El.remove("")
        return (Arr_Element_El)
    def Handling_Data_Element(self,Arr_Elements):
        Handling_DataS_Tr_Ap = []
        for index_Arr,Arr_Element in enumerate(Arr_Elements,0):
            Arr_Index_Element = [index for index,vt in enumerate(Arr_Element,0) if vt in self.Arr_characters_special]
            Handling_DataS_Tr_eD = self.Handling_Data_Tr(Arr_Index_Element,Arr_Element)
            if str(index_Arr) in self.KeepValueNotChange:
                Handling_DataS_Tr_Ap.append(Arr_Element)
            else:
             Handling_DataS_Tr_Ap.append(Handling_DataS_Tr_eD)  
        return Handling_DataS_Tr_Ap
    def CreateDict(self):
        dictionary_Arr = []
        for i in range(4,len(self.ArrReturn),1):
            values = self.ArrReturn[i]
            Handling_Element= self.Handling_Data_Element(values)
            #Handling_Element= Handling_Data_Element(values)
            dictionary = dict(zip(self.keys, Handling_Element))
            dictionary_Arr.append(dictionary)
        return dictionary_Arr
    def Handling_DataS_Tr_For_Case_Expect(self):
        Handling_DataS_Tr_For_Case_Expected = []
        for ElementStr in self.Check_Con_To_Case_Expect:
            Arr_Index_Element = [index for index,vt in enumerate(ElementStr,0) if vt in self.Arr_characters_special]
            Value_Check_For_For_Case_Expect = self.Handling_Data_Tr(Arr_Index_Element,ElementStr)
            Handling_DataS_Tr_For_Case_Expected.append(Value_Check_For_For_Case_Expect)
        return Handling_DataS_Tr_For_Case_Expected
# remove Duplicate element from list 
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 
def func(alist):
    return zip(alist, alist[1:])
"""