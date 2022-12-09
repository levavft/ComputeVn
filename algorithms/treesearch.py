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

class _TreeSearchAlgorithmSingleton(VNAlgorithmBase):
    def __init__(self):
        self.name = "Tree search algorithm"

    @timed
    def memoized_calculate_v(self, g: AbelianGroup, max_tries: int = 10) -> int:
        
        m = SummableMultiset()
        
        return None
        
TreeSearchAlgorithm = _TreeSearchAlgorithmSingleton()