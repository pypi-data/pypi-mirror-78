class bidirectional_iterator(object):
    def __init__(self, collection):
        self.collection = collection
        self.index = 0
        self.k = 0 
        self.n = 0

    def next(self):
        if self.n != 0:
            self.index =  self.index + 1
            self.n = 0
        result = self.collection[self.index]
        self.index = self.index + 1
        self.k += 1
        if self.index > len(self.collection)- 1:
            self.index = 0
        return result

    def prev(self):
        self.n += 1
        if self.k != 0:
            self.index =  self.index - 2
            self.k = 0
        else:
            self.index =  self.index - 1
        if self.index < 0:
            self.index = len(self.collection)- 1
        return self.collection[self.index]

    def __iter__(self):
        return self