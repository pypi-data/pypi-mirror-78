class ValComparator:
    def __init__(self, x1, x2):
        self.x1 = float(x1)
        self.x2 = float(x2)
    
    def greater(self):
        return self.x1 > self.x2
    
    def equal(self):
        return self.x1 == self.x2
    
    def less(self):
        return self.x1 < self.x2