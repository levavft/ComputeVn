from multiset import Multiset

class SummableMultiset(Multiset):
    def sum(self):
        return sum( [k * v for k, v in self.items()] )
        
    def verify_is_annoying(self):
        return False