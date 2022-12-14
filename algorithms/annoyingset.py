#   
#   
#   Implementation of https://cs.stackexchange.com/questions/155871/finding-all-zero-sums-of-length-m-and-checking-for-zero-subsums-on-an-abelian-gr
#   
#   

from classes.helpers.timer import Timer
from classes.abeliangroup import AbelianGroup
from classes.multisetextensions import SummableMultiset
from algorithms.algorithmbase import VNAlgorithmBase

# make decorator
timed = Timer.measure
sum = timed(sum)


class ExtendedSummableMultisetPowerset:
    def __init__(self):
        self.multisets_nontrivial = []
        self.master_multiset = SummableMultiset()

    def add_element(self, e):
        to_append = self.multisets_nontrivial.copy()
        # print("has: ", self.multisets)
        [m.add(e) for m in self.multisets_nontrivial]
        self.multisets_nontrivial.append(SummableMultiset([e]))
        self.multisets_nontrivial.extend(to_append)
        self.multisets_nontrivial.append(self.master_multiset)
        self.master_multiset.add(e)
        # print("has: ", self.multisets)

    def is_annoying(self):
        return not any(map(SummableMultiset.sums_to_zero, self.multisets_nontrivial))

    def __repr__(self):
        return str(self.multisets_nontrivial)

    def copy(self):
        re = ExtendedSummableMultisetPowerset()
        [re.multisets_nontrivial.append(m.copy()) for m in self.multisets_nontrivial]
        return re


class bruh(Exception):
    pass


# doesn't work
class _AnnoyingSetAlgorithmSingleton(VNAlgorithmBase):
    def __init__(self):
        self.name = "Annoying set algorithm"

    @timed
    def memoized_calculate_v(self, g: AbelianGroup, max_tries: int = 10) -> int:

        size = 0
        annoying_sets_current = [ExtendedSummableMultisetPowerset()]

        while len(annoying_sets_current) > 0:
            annoying_sets_new = []

            # print("CURRENT: ", annoying_sets_current)

            for e in g.elements(include_zero=False):
                for m in annoying_sets_current:

                    # print("CURRENT: ", annoying_sets_current)
                    # print("CHECKING: ", e, m.multisets)

                    new_m = m.copy()
                    new_m.add_element(e)

                    if new_m.is_annoying():
                        annoying_sets_new.append(new_m)
                        # print("ADDED: ", new_m.multisets)

                    # print("NEW (TEMP): ", annoying_sets_new)

            # print("NEW: ", annoying_sets_new)
            annoying_sets_current = annoying_sets_new

            size += 1

            if size > max_tries:
                raise bruh

        return size


AnnoyingSetAlgorithm = _AnnoyingSetAlgorithmSingleton()
