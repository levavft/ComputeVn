#
#
#   Implementation of https://cs.stackexchange.com/questions/155871/finding-all-zero-sums-of-length-m-and-checking-for-zero-subsums-on-an-abelian-gr
#
#

from classes.helpers.timer import Timer
from classes.abeliangroup import AbelianGroup
from classes.multisetextensions import SumMultiSet
from algorithms.algorithmbase import VNAlgorithmBase

# make decorator
timed = Timer.measure
sum = timed(sum)


class _AnnoyingSetAlgorithmLevavsTrySingleton(VNAlgorithmBase):
    def __init__(self):
        self.name = "Annoying set algorithm"

    @timed
    def memoized_calculate_v(self, g: AbelianGroup, max_tries: int = 10) -> int:

        size = 0
        Z = [SumMultiSet(g)]

        while True:
            Z_prime = [z.added(x) for z in Z for x in g.elements(include_zero=False)[z.maximal_element_index:]]
            Z = [z for z in Z_prime if not z.has_zero_sub_multiset_sum()]
            size += 1
            if size >= 2 and all(map(lambda x: not x.sums_to_zero(), Z)):
                break
            if size > max_tries:
                return float("inf")

        return size - 1


AnnoyingSetAlgorithmLevavsTry = _AnnoyingSetAlgorithmLevavsTrySingleton()