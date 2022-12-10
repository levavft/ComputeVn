#   
#   
#   Implementation of https://cs.stackexchange.com/questions/155871/finding-all-zero-sums-of-length-m-and-checking-for-zero-subsums-on-an-abelian-gr
#   
#   

from classes.helpers.timer      import Timer
from classes.abeliangroup       import AbelianGroup
from classes.multisetextensions import SummableMultiset
from algorithms.algorithmbase   import VNAlgorithmBase

# make decorator
timed = Timer.measure
sum = timed(sum)


class ExtendedSummableMultisetPowerset:
    def __init__(self):
        self.multisets = set()
        
    def add_element(self, e):
        to_append = self.multisets.copy()
        #print("has: ", self.multisets)
        [m.add(e) for m in self.multisets]
        self.multisets.add(SummableMultiset([e]))
        self.multisets = self.multisets.union(to_append)
        #print("has: ", self.multisets)
        
    def is_annoying(self):
        return not any( map( SummableMultiset.sums_to_zero, self.multisets ) )
        
    def __repr__(self):
        return str(self.multisets)
        
    def copy(self):
        re = ExtendedSummableMultisetPowerset()
        [re.multisets.add(m.copy()) for m in self.multisets]
        return re

class bruh(Exception):
    pass

class _TreeSearchAlgorithmSingleton(VNAlgorithmBase):
    def __init__(self):
        self.name = "Tree search algorithm"

    @timed
    def memoized_calculate_v(self, g: AbelianGroup, max_tries: int = 10) -> int:
        
        size = 0
        annoying_sets_current = [ExtendedSummableMultisetPowerset()]
        
        while len(annoying_sets_current) > 0:
            annoying_sets_new = []
            
            #print("CURRENT: ", annoying_sets_current)
            
            for e in g.elements(include_zero = False):
                for m in annoying_sets_current:
                
                    #print("CURRENT: ", annoying_sets_current)
                    #print("CHECKING: ", e, m.multisets)
                
                    new_m = m.copy()
                    new_m.add_element(e)
                    
                    if( new_m.is_annoying() ):
                        annoying_sets_new.append(new_m)
                        #print("ADDED: ", new_m.multisets)
                        
                    #print("NEW (TEMP): ", annoying_sets_new)
            
            #print("NEW: ", annoying_sets_new)
            annoying_sets_current = annoying_sets_new
            
            size += 1
        
            if(size > 10):
                raise bruh
        
        return size
        
TreeSearchAlgorithm = _TreeSearchAlgorithmSingleton()