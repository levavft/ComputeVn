from sympy import lcm, primefactors
from multiset import Multiset
from functools import cache


class AbelianGroup:
    def __init__(self, limit: tuple):
        # There probably is a type of iterator that has the same functionality and speed as saving an element order map
        # like this, if this code enters sympy its worth looking up the official method.
        self.limit = tuple(sorted(limit))
        self.limit_breaks = self._get_limit_breaks()
        self.non_zero_elements = self._elements(include_zero=False)
        self.with_zero_elements = self._elements()
        self.element_index_map = {e: i for i, e in enumerate(self.non_zero_elements)}
        self.zero = self._zero()
        self.element_index_map[self.zero] = -float(
            "inf")  # there's a need to rethink what I do with the zero of our abelian groups...
        self.equivalence_classes_to_elements_map = dict()
        self.__generate_equivalence_classes()
        self.equivalence_classes = list(sorted(self.equivalence_classes_to_elements_map.keys()))

    def __generate_equivalence_classes(self):
        for element in self.with_zero_elements:
            equiv = element.equivalence_class()
            if equiv not in self.equivalence_classes_to_elements_map:
                self.equivalence_classes_to_elements_map[equiv] = set()
            self.equivalence_classes_to_elements_map[equiv].add(element)

    def _get_limit_breaks(self):
        # limit breaks aim to describe runs of the same number in 'self.limit'.
        # if the limit is (a,a,a,b,b,b,c,c,d) the limit breaks are: [(0, 3), (3, 6), (6, 8), (8, None)]
        # this is useful since we can slice our group elements at the limit breaks.
        # for example: 'elem[8: None]' is the same as 'elem[8:]'
        limits = [0] + [i for i in range(1, len(self.limit)) if self.limit[i - 1] != self.limit[i]] + [None]
        return [(limits[i], limits[i + 1]) for i in range(len(limits) - 1)]

    def _elements(self, include_zero=True):
        result = [tuple()]
        for i in range(len(self.limit)):
            result = [(*tup, j) for tup in result for j in range(self.limit[i])]
        return tuple(AbelianGroupElement(r, self) for r in result if include_zero or not sum(r) == 0)

    def elements(self, include_zero=True):
        if include_zero:
            return self.with_zero_elements
        return self.non_zero_elements

    def maximal_element_order(self):
        return lcm(self.limit)

    def is_pgroup(self):
        return len(set.union(*[set(primefactors(i)) for i in set(self.limit)])) == 1

    def as_summand_orders(self):
        return self.limit

    def summand_count(self):
        return len(self.limit)

    def _zero(self):
        return AbelianGroupElement((0,) * len(self.limit), self)

    def __add__(self, other):
        assert isinstance(other, AbelianGroup)
        return AbelianGroup((*self.limit, *other.limit))

    def __eq__(self, other):
        assert isinstance(other, AbelianGroup)
        return self.limit == other.limit

    def __hash__(self):
        return hash(f"AbelianGroup(<{self.limit}>)")

    def __repr__(self):
        return f"<{self.limit}>"

    def __str__(self):
        return f"<{self.limit}>"


class AbelianGroupElement:
    def __init__(self, value: tuple, g: AbelianGroup):
        """
        examples for the case of the element (2, 3) in C_4+C_4
        :param value: (2, 3)
        :param limit: (4, 4)
        """
        self.value = value
        self.g = g
        self._hash = None
        self._equivalence_class = None

    def __zero_like(self):
        return self.g.zero

    def __interact(self, other):
        if other == 0:
            other = self.__zero_like()
        return other

    @cache
    def equivalence_class(self):
        return tuple(tuple(sorted([(k, v) for k, v in Multiset(self.value[i: j]).items()], key=lambda x: x[0]))
                     for i, j in self.g.limit_breaks)

    @cache
    def __add__(self, other):
        return AbelianGroupElement(
                tuple((self.value[i] + self.__interact(other).value[i]) % self.g.limit[i] for i in range(len(self.value))), self.g)

    @cache
    def __radd__(self, other):
        return self.__add__(other)

    @cache
    def __sub__(self, other):
        return AbelianGroupElement(
                tuple((self.value[i] - self.__interact(other).value[i]) % self.g.limit[i] for i in range(len(self.value))), self.g)

    def __neg__(self):
        return self.__zero_like() - self

    def __eq__(self, other):
        other = self.__interact(other)
        return (self.value, self.g) == (other.value, other.g)

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(f"AbelianGroupElement<{(self.value, self.g)}>")
        return self._hash

    def __repr__(self):
        return str(self.value)
