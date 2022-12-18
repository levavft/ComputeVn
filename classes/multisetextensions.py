import copy

from multiset import Multiset, FrozenMultiset
from classes.abeliangroup import AbelianGroup, AbelianGroupElement
from classes.helpers.timer import Timer
from functools import cache
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
    def __init__(self, g: AbelianGroup, parent=None):
        # Due to the nature of SumMultiSet, it is better to add one element at a time,
        # hence it is initiated with no elements.
        self.elements = Multiset() if parent is None else Multiset(parent.elements)
        self.equivalence_classes = Multiset() if parent is None else Multiset(parent.equivalence_classes)
        self.tracked_sum = 0 if parent is None else parent.tracked_sum
        self.sub_multiset_sums = set() if parent is None else set(parent.sub_multiset_sums)
        self.g = g
        # it can be assumed that this is the index of the last inserted element.
        self.maximal_element_index = 0 if parent is None else parent.maximal_element_index

        self._prehash = None

    def add(self, e: AbelianGroupElement):
        # the multiplicity variable is needed because of super(), but shouldn't exist for us.
        if len(self.elements) > 0:
            self.sub_multiset_sums = self.sub_multiset_sums | {s + e for s in self.sub_multiset_sums} | {self.tracked_sum, e}
        self.maximal_element_index = self.g.element_index_map[e]
        self.tracked_sum = self.tracked_sum + e
        self.elements.add(e)
        self.equivalence_classes.add(e.equivalence_class())
        self._prehash = None

    def get_sum(self):
        return self.tracked_sum

    def sums_to_zero(self):
        return self.tracked_sum == 0

    def has_zero_sub_multiset_sum(self):
        return self.g.zero in self.sub_multiset_sums or 0 in self.sub_multiset_sums

    def added(self, e):
        # this is inline addition of an element, the name is based on python's sorted/sort distinction.
        new = SumMultiSet(self.g, parent=self)
        new.add(e)
        return new

    def __hash__(self):
        def h(equivalence_class):
            return tuple(sorted(Multiset(self.elements[element] for element in
                                         self.g.equivalence_classes_to_elements_map[equivalence_class] if element in
                                         self.elements).values()))
        if self._prehash is None:
            self._prehash = [str(h(equiv)) for equiv in self.g.equivalence_classes]
        return hash(tuple(self._prehash))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return str(self.elements)

    def __repr__(self):
        return str(self)
