from sympy import lcm, primefactors
from multiset import Multiset


class AbelianGroup:
    def __init__(self, limit: tuple):
        # There probably is a type of iterator that has the same functionality and speed as saving an element order map
        # like this, if this code enters sympy its worth looking up the official method.
        # TODO: it is likely that elements are created an excessive amount of times. due the elements becoming more
        #  and more complex it is imperative to create a model in which elements are never recreated.
        self.limit = tuple(sorted(limit))
        self.limit_breaks = self._get_limit_breaks()
        self.non_zero_elements = self._elements(include_zero=False)
        self.with_zero_elements = self._elements()
        self.element_index_map = {e: i for i, e in enumerate(self.non_zero_elements)}
        self.zero = self._zero()
        self.element_index_map[self.zero] = -float(
            "inf")  # there's a need to rethink what I do with the zero of our abelian groups...
        self.sum_map = dict()
        self.diff_map = dict()
        self.equivalence_classes_to_elements_map = dict()
        self.generate_equivalence_classes()

    def generate_equivalence_classes(self):
        for element in self.with_zero_elements:
            equiv = element.equivalence_class()
            if equiv not in self.equivalence_classes_to_elements_map:
                self.equivalence_classes_to_elements_map[equiv] = set()
            self.equivalence_classes_to_elements_map[equiv].add(element)

    def _get_limit_breaks(self):
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
        assert isinstance(other, AbelianGroupElement) or other == 0
        if other == 0:
            other = self.__zero_like()
        assert self.g == other.g
        return other

    def equivalence_class(self):
        if self._equivalence_class is None:
            self._equivalence_class = tuple(tuple(sorted([(k, v) for k, v in Multiset(self.value[i: j]).items()]
                                                         , key=lambda x: x[0]))
                                            for i, j in self.g.limit_breaks)
        return self._equivalence_class

    def __add__(self, other):
        if (self, other) not in self.g.sum_map:
            other_fixed = self.__interact(other)
            self.g.sum_map[(self, other)] = AbelianGroupElement(
                tuple((self.value[i] + other_fixed.value[i]) % self.g.limit[i] for i in range(len(self.value))), self.g)
        return self.g.sum_map[(self, other)]

    def __mul__(self, other):
        assert isinstance(other, int)
        s = self
        for i in range(other - 1):
            s = s + self
        return s

    def __rmul__(self, other):
        return self.__mul__(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if (self, other) not in self.g.diff_map:
            other_fixed = self.__interact(other)
            self.g.diff_map[(self, other)] = AbelianGroupElement(
                tuple((self.value[i] - other_fixed.value[i]) % self.g.limit[i] for i in range(len(self.value))), self.g)
        return self.g.diff_map[(self, other)]

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
