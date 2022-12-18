import copy

from multiset import Multiset
from classes.abeliangroup import AbelianGroup
from classes.helpers.timer import Timer
from random import getrandbits

# make decorator
timed = Timer.measure
copy.copy = timed(copy.copy)


class SummableMultiset(Multiset):
    def __init__(self, em=None):
        if em is None:
            em = []
        self.tracked_sum = sum(em)
        super().__init__(em)

    def add(self, e, multiplicity=1):
        # print(self.tracked_sum, e)
        self.tracked_sum = self.tracked_sum + e
        # print(self.tracked_sum, e)
        super().add(e, multiplicity=multiplicity)

    def get_sum(self):
        return self.tracked_sum

    def sums_to_zero(self):
        # print(self.items(), self.tracked_sum)
        return self.tracked_sum == 0

    # # only for abelian case
    # def __hash__(self):
    #     # return hash(self.tracked_sum)
    #     return hash(str(self.values))

    def add_inline(self, em):
        mc = self.copy()
        mc.add(em)
        return mc


class SumMultiSet:
    def __init__(self, g: AbelianGroup):
        # Due to the nature of SumMultiSet, it is better to add one element at a time,
        # hence it is initiated with no elements.
        self.elements = Multiset()
        self.tracked_sum = 0
        self.sub_multiset_sums = set()
        self.g = g
        # it can be assumed that this is the index of the last inserted element.
        self.maximal_element_index = 0
        self._hash = getrandbits(64)

    def add(self, e):
        # the multiplicity variable is needed because of super(), but shouldn't exist for us.
        if len(self.elements) > 0:
            self.sub_multiset_sums = self.sub_multiset_sums | {s + e for s in self.sub_multiset_sums} | {self.tracked_sum, e}
        self.maximal_element_index = self.g.element_index_map[e]
        self.tracked_sum = self.tracked_sum + e
        self.elements.add(e)

    def get_sum(self):
        return self.tracked_sum

    def sums_to_zero(self):
        return self.tracked_sum == 0

    def has_zero_sub_multiset_sum(self):
        return self.g.zero in self.sub_multiset_sums

    def added(self, e):
        # this is inline addition of an element, the name is based on python's sorted/sort distinction.
        new = copy.copy(self)
        new.add(e)
        return new

    def __hash__(self):
        return self._hash

    def __str__(self):
        return str(self.elements)

    def __repr__(self):
        return str(self)
