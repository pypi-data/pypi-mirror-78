class towlist:
    """handling 2 list """
    def __init__ (self, list1= None, list2 = None):
        self.list1 = list1
        self.list2 = list2

    def subtracttowlist(self):
        """sub tract 2 list"""
        difference = []
        #initialization of result list
        zip_object = zip(self.list1, 
                        self.list2)
        for list1_i, list2_i in zip_object:
            difference.append(list1_i-list2_i)
        return difference

    def plustracttowlist(self):
        """plus tract 2 list"""
        difference = []
        #initialization of result list
        zip_object = zip(self.list1, 
                        self.list2)
        for list1_i, list2_i in zip_object:
            difference.append(list1_i+list2_i)
        return difference

