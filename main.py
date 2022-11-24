from itertools import combinations
from sympy import lcm
import time


TOTAL_TIME = dict()


def timeit(func):
    """
    Decorator for measuring function's running time.
    Includes time of inner function calls, hence not suitable for recursion.
    """
    def measure_time(*args, **kw):
        fname = func.__qualname__
        if fname not in TOTAL_TIME:
            TOTAL_TIME[fname] = 0
        start_time = time.time()
        result = func(*args, **kw)
        TOTAL_TIME[fname] += time.time() - start_time
        return result

    return measure_time


class AbelianGroup:
    def __init__(self, limit: tuple):
        # There probably is a type of iterator that has the same functionality and speed as saving an element order map
        # like this, if this code enters sympy its worth looking up the official method.
        self.limit = limit
        self.non_zero_elements = self.elements(include_zero=False)
        self.order_map = {e: i for i, e in enumerate(self.non_zero_elements)}

    @timeit
    def elements(self, include_zero=True):
        result = [tuple()]
        for i in range(len(self.limit)):
            result = [(*tup, j) for tup in result for j in range(self.limit[i])]
        return tuple(AbelianGroupElement(r, self.limit) for r in result if include_zero or not sum(r) == 0)

    def maximal_element_order(self):
        return lcm(self.limit)

    def zero(self):
        return AbelianGroupElement((0, ) * len(self.limit), self.limit)

    def __add__(self, other):
        assert isinstance(other, AbelianGroup)
        return AbelianGroup((*self.limit, *other.limit))

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
        return self.value == other.value

    def __hash__(self):
        return hash((self.value, self.limit))

    def __repr__(self):
        return str(self.value)


@timeit
def powerset(iterable: tuple):
    for r in range(len(iterable) + 1):
        for combination in combinations(iterable, r):
            yield combination


@timeit
def has_zero_subsum(summands: tuple, g: AbelianGroup):
    for s in powerset(summands):
        if len(s) in {len(summands), 0}:
            continue
        if sum(s, start=g.zero()) == g.zero():
            return True
    return False


@timeit
def memoized_group_check(g: AbelianGroup, m: int, memo: set = None, summands: tuple = None) -> bool:
    """
    TODO: rename function.
    TODO: reorder the logic of this function. (many lines can be save at a tiny optimization cost)
    TODO: create a non-recursive version as recursions are horrid in python.
    :param g: an abelian group
    :param m: a natural number
    :param memo:
    :param summands:
    :return: True if V_m holds for g
    """

    assert g.maximal_element_order() <= m and m > 1
    if memo is None:
        memo = set()
    if summands is None:
        for e in g.non_zero_elements:
            if not memoized_group_check(g, m, memo, (e, )):
                return False
        return True

    if len(summands) == m - 1:
        summands = (*summands, -sum(summands, start=g.zero()))
        if summands[-1] == g.zero() or g.order_map[summands[-1]] < g.order_map[summands[-2]]:
            return True
        return has_zero_subsum(summands, g)

    for i in range(g.order_map[summands[-1]], len(g.non_zero_elements)):
        new_summands = (*summands, g.non_zero_elements[i])
        if new_summands in memo:
            continue
        if has_zero_subsum(new_summands, g):
            memo.add(new_summands)
            continue
        if not memoized_group_check(g, m, memo, new_summands):
            return False

    return True


@timeit
def memoized_calculate_v(g: AbelianGroup, max_tries: int = 10) -> int:
    """
    TODO: rename this function.
    :param g: an abelian group
    :param max_tries: number of V_m's to check
    :return: V(G)
    """
    meo = g.maximal_element_order()
    memo = set()
    for m in range(meo + 1, meo + max_tries + 1):
        result = memoized_group_check(g, m, memo)
        if result:
            return m - 1


@timeit
def main():
    # to get an insanely detailed time analysis run: python -m cProfile main.py
    AB = AbelianGroup
    group_values = {AB((2,)): 2,
                    AB((3,)): 3, AB((2, 2)): 3,
                    AB((4,)): 4, AB((2, 2, 2)): 4,
                    AB((5,)): 5, AB((3, 3)): 5, AB((2, 4)): 5, AB((2, 2, 2, 2)): 5,
                    AB((6,)): 6, AB((2, 2, 4)): 6,
                    AB((7,)): 7, AB((4, 4)): 7, AB((2, 6)): 7,
                    }
    for g in group_values.keys():
        print(f"V_{memoized_calculate_v(g)} holds for {g}")


if __name__ == '__main__':
    main()
    for fname, time in TOTAL_TIME.items():
        print("Processing time of %s(): %.2f seconds." % (fname, time))
