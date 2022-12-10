from multiset import Multiset


class SummableMultiset(Multiset):
    def __init__(self, em=None):
        if em is None:
            em = []
        self.tracked_sum = sum(em)
        super().__init__(em)

    def add(self, e, multiplicity=1):
        #print(self.tracked_sum, e)
        self.tracked_sum = self.tracked_sum + e
        #print(self.tracked_sum, e)
        super().add(e, multiplicity=multiplicity)

    def get_sum(self):
        return self.tracked_sum
        
    def sums_to_zero(self):
        #print(self.items(), self.tracked_sum)
        return self.tracked_sum == 0
        
    # only for abelian case
    def __hash__(self):
        return hash(self.tracked_sum)
        
    def add_inline(self, em):
        mc = self.copy()
        mc.add(em)
        return mc
