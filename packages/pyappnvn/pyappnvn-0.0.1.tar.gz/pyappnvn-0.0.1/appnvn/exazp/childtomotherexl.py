from pynvn.path.ppath import PathSteel
from appnvn.exazp.hdata import hdata
class kidtomother:
    def __init__(self,pathfolder = None,
                fileparent = "WHITEX - TONG HOP NGAN SACH.xlsx",
                filekid = "AZB-INPUT.xlsx",
                subfolderinput = "0.input",
                subfolderoutput = "1.output",
                kipnamesheet = ["AZB-20","AZB-40","AZB-50","AZB-60","AZB-70","AZB-80"],
                runforexcel = "both"
                ):
                self.fileparent = fileparent
                self.pathfolder = pathfolder
                self.filekid = filekid
                self.subfolderinput = subfolderinput
                self.subfolderoutput = subfolderoutput
                self.runforexcel = runforexcel
                self.kipnamesheet = kipnamesheet

                self.ps = PathSteel(dir_path=self.pathfolder,
                                    Is_Directory_Path_To_SubFolder=True,
                                    subfolder=self.subfolderinput,
                                    FileName=self.filekid)
                # return file kid 
                self.pathkid =  self.ps.refpath()
                # return fileparent 
                self.ps.subfolder = self.subfolderoutput
                self.ps.FileName = self.fileparent
                self.pathparent = self.ps.refpath()

                self.namesheet = ["AZB-10",
                                    "AZB-20",
                                    "AZB-30",
                                    "AZB-40",
                                    "AZB-50",
                                    "AZB-60",
                                    "AZB-70",
                                    "AZB-80"]
                #set keysheet 
                self.keysheet = {self.namesheet[0]:[41,3,18,None,41,3,18,None],\
                                self.namesheet[1]:[41,3,18,None,41,3,18,None],\
                                self.namesheet[2]:[6,4,19,None,6,4,19,None],\
                                self.namesheet[3]:[41,3,18,None,41,3,18,None],\
                                self.namesheet[4]:[41,3,18,None,41,3,18,None],\
                                self.namesheet[5]:[41,3,18,None,41,3,18,None],\
                                self.namesheet[6]:[41,3,18,None,41,3,18,None],\
                                self.namesheet[7]:[41,3,18,None,41,3,18,None]}
                
    def transferdatatoparent(self):
        """ tranfer data to parent """
        for ns in self.namesheet:
            vals = self.keysheet.get(ns)
            if ns in self.kipnamesheet:
                continue
            else:
                self.ht = hdata (pathfile=self.pathkid,sheetname=ns,\
                                rowindexstart=vals[0],columnmh=vals[1],\
                                columntotp=vals[2],valuecelltoskip=vals[3],\
                                pathfile_to=self.pathparent,sheetname_to=ns,\
                                rowindexstart_to=vals[4],columnmh_to=vals[5],\
                                columntotp_to=vals[6],valuecelltoskip_to=vals[7]
                                )
                if self.runforexcel == "kid":
                    self.ht.hldatakid()
                elif self.runforexcel == "mother":
                    self.ht.hldataparent()
                else:
                    self.ht.hldatakid()
                    self.ht.hldataparent()
