from sympy import lcm


class AbelianGroup:
    def __init__(self, limit: tuple):
        # There probably is a type of iterator that has the same functionality and speed as saving an element order map
        # like this, if this code enters sympy its worth looking up the official method.
        self.limit = limit
        self.non_zero_elements = self.elements(include_zero=False)
        self.order_map = {e: i for i, e in enumerate(self.non_zero_elements)}
        self.zero = self._zero()
        self.order_map[self.zero] = -float("inf")  # there's a need to rethink what I do with the zero of our abelian groups...

    def elements(self, include_zero=True):
        result = [tuple()]
        for i in range(len(self.limit)):
            result = [(*tup, j) for tup in result for j in range(self.limit[i])]
        return tuple(AbelianGroupElement(r, self.limit) for r in result if include_zero or not sum(r) == 0)

    def maximal_element_order(self):
        return lcm(self.limit)

    def _zero(self):
        return AbelianGroupElement((0, ) * len(self.limit), self.limit)

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


class AbelianGroupElement:
    def __init__(self, value: tuple, limit: tuple):
        """
        examples for the case of the element (2, 3) in C_4+C_4
        :param value: (2, 3)
        :param limit: (4, 4)
        """
        self.value = value
        self.limit = limit

    def __zero_like(self):
        return AbelianGroupElement((0, ) * len(self.limit), self.limit)

    def __interact(self, other):
        assert isinstance(other, AbelianGroupElement) or other == 0
        if other == 0:
            other = self.__zero_like()
        assert self.limit == other.limit
        return other

    def __add__(self, other):
        other = self.__interact(other)
        return AbelianGroupElement(tuple((self.value[i] + other.value[i]) % self.limit[i] for i in range(len(self.value))),
                                   self.limit)

    def __sub__(self, other):
        other = self.__interact(other)
        return AbelianGroupElement(tuple((self.value[i] - other.value[i]) % self.limit[i] for i in range(len(self.value))),
                                   self.limit)

    def __neg__(self):
        return self.__zero_like() - self

    def __eq__(self, other):
        other = self.__interact(other)
        return (self.value, self.limit) == (other.value, other.limit)

    def __hash__(self):
        return hash(f"AbelianGroupElement<{(self.value, self.limit)}>")

    def __repr__(self):
        return str(self.value)


# groups and their values are taken from citation 6 of the paper we're looking at.
AB = AbelianGroup
group_values = {AB((2, )): 2,
                AB((3, )): 3, AB((2, 2)): 3,
                AB((4, )): 4, AB((2, 2, 2)): 4,
                AB((5, )): 5, AB((3, 3)): 5, AB((2, 4)): 5, AB((2, 2, 2, 2)): 5,
                AB((6, )): 6, AB((2, 2, 4)): 6, AB(tuple([2] * 5)): 6,
                AB((7, )): 7, AB((4, 4)): 7, AB((2, 6)): 7,
                }


# too slow for now
# additional_group_values = {
#
#     AB((3, 3, 3)): 7, AB((2, 2, 2, 4)): 7, AB([2] * 6): 7
# }
