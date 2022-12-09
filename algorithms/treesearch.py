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
        self.multisets = []
        
    def add_element(self, e, group_elements):
        [m.add(e) for m in self.multisets]
        self.multisets.append(SummableMultiset([e]))
        [self.multisets.append(SummableMultiset([g])) for g in group_elements]
        
    def is_annoying(self):
        return any( map( SummableMultiset.sum, self.multisets ) )


class _TreeSearchAlgorithmSingleton(VNAlgorithmBase):
    def __init__(self):
        self.name = "Tree search algorithm"

    @timed
    def memoized_calculate_v(self, g: AbelianGroup, max_tries: int = 10) -> int:
        
        size = 0
        annoying_sets_current = [ExtendedSummableMultisetPowerset()]
        group_elements = g.elements(include_zero = False)
        
        while len(annoying_sets_current) > 0:
            
            annoying_sets_new = []
            
            for e in group_elements:
                for m in annoying_sets_current:
                
                    new_m = ExtendedSummableMultisetPowerset()
                    new_m.multisets = m.multisets
                    new_m.add_element(e, group_elements)
                    
                    if( new_m.is_annoying( )):
                        annoying_sets_new.append(new_m)
            
            annoying_sets_current = annoying_sets_new
            
            size += 1
        
        return size
        
TreeSearchAlgorithm = _TreeSearchAlgorithmSingleton()