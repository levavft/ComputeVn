#   
#   
#   Relocation of old code from main.py
#   
#   

from itertools import combinations
from multiset import Multiset, FrozenMultiset as fms

from classes.helpers.timer import Timer
from classes.abeliangroup import AbelianGroup
from algorithms.algorithmbase import VNAlgorithmBase

# make decorator
timed = Timer.measure
sum = timed(sum)
fms = timed(fms)


@timed
def relevant_powerset(iterable: tuple):
    for r in range(2, len(iterable) // 2 + 1):
        for combination in combinations(iterable, r):
            yield combination


@timed
def get_similar_sums(summands: tuple, zero_sum: tuple) -> set:
    diff_tuple = tuple(Multiset(summands).difference(Multiset(zero_sum)))
    return {fms(zero_sum), fms(diff_tuple)}


@timed
def has_zero_subsum(summands: tuple, g: AbelianGroup, memo: set) -> bool:
    for s in relevant_powerset(summands):
        if sum(s, start=g.zero) == g.zero:
            memo.update(get_similar_sums(summands, s))
            return True
    return False


def memoized_group_check(g: AbelianGroup, m: int, memo: set = None, summands: tuple = None) -> bool:
    """
    TODO: rename function.
    TODO: create a non-recursive version as recursions are horrid in python.
    :param g: an abelian group
    :param m: a natural number
    :param memo:
    :param summands:
    :return: True if V_m holds for g
    """

    assert m > 1 and g.maximal_element_order() <= m
    if memo is None:
        memo = set()
    if summands is None:
        summands = tuple()
    if fms(summands) in memo:
        return True
    if len(summands) > 0 and sum(summands, start=g.zero) == g.zero:  # this removes about a 1/4rth of the runtime.
        memo.add(fms(summands))
        return True

    if len(summands) == m - 1:
        summands = (*summands, -sum(summands, start=g.zero))
        if summands[-1] == g.zero or g.element_index_map[summands[-1]] < g.element_index_map[summands[-2]]:
            return True
        return has_zero_subsum(summands, g, memo)

    start = 0 if len(summands) == 0 else g.element_index_map[summands[-1]]
    for i in range(start, len(g.non_zero_elements)):
        new_summands = (*summands, g.non_zero_elements[i],)
        if has_zero_subsum(new_summands, g, memo):
            memo.add(fms(new_summands))
            continue
        if not memoized_group_check(g, m, memo, new_summands):
            return False
    return True


class _NaiveAlgorithmSingleton(VNAlgorithmBase):
    def __init__(self):
        self.name = "Naive algorithm"

    @timed
    def memoized_calculate_v(self, g: AbelianGroup, max_tries: int = 10) -> int:
        """
        TODO: rename this function.
        TODO: move above methods to the right place
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


NaiveAlgorithm = _NaiveAlgorithmSingleton()
