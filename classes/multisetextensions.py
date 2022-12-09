from multiset import Multiset

class SummableMultiset(Multiset):
    def __init__(self, em = []):
        super().__init__(em)

    def sum(self):
        print(list(self.items()))
        return sum( [k * v for k, v in self.items()] )
        
    def add_inline(self, em):
        mc = self.copy()
        mc.add(em)
        return mc