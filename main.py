from itertools import combinations, permutations
import time
from multiset import Multiset
from abeliangroup import AbelianGroup, group_values
from sympy import primefactors


TOTAL_MEASURE = dict()


def measure(func):
    """
    Decorator for measuring function's running time.
    Includes time of inner function calls, hence not suitable for recursion.
    """
    def _measure(*args, **kw):
        fname = func.__qualname__
        if fname not in TOTAL_MEASURE:
            TOTAL_MEASURE[fname] = {'Wall Time': 0, 'CPU Time': 0, 'Runs': 0}
        start_wall_time = time.time()
        start_cpu_time = time.process_time()
        result = func(*args, **kw)
        TOTAL_MEASURE[fname]['Wall Time'] += time.time() - start_wall_time
        TOTAL_MEASURE[fname]['CPU Time'] += time.process_time() - start_cpu_time
        TOTAL_MEASURE[fname]['Runs'] += 1
        return result

    return _measure


sum = measure(sum)


@measure
def relevant_powerset(iterable: tuple):
    for r in range(1, len(iterable) // 2 + 1):
        for combination in combinations(iterable, r):
            yield combination


@measure
def get_similar_sums(summands: tuple, zero_sum: tuple) -> set:
    diff_tuple = tuple(Multiset(summands).difference(Multiset(zero_sum)))
    return set(permutations(zero_sum)).union(permutations(diff_tuple))


@measure
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
    if summands in memo:
        return True
    if len(summands) > 0 and sum(summands, start=g.zero) == g.zero:  # this removes about a 1/4rth of the runtime.
        memo.add(summands)
        # memo.update(permutations(summands))
        return True

    if len(summands) == m - 1:
        summands = (*summands, -sum(summands, start=g.zero))
        if summands[-1] == g.zero or g.order_map[summands[-1]] < g.order_map[summands[-2]]:
            return True
        return has_zero_subsum(summands, g, memo)

    start = 0 if len(summands) == 0 else g.order_map[summands[-1]]
    for i in range(start, len(g.non_zero_elements)):
        new_summands = (*summands, g.non_zero_elements[i], )
        if has_zero_subsum(new_summands, g, memo):
            memo.add(new_summands)
            # memo.update(permutations(summands))
            continue
        if not memoized_group_check(g, m, memo, new_summands):
            return False
    return True


@measure
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


def calculate_v_if_solved(g: AbelianGroup):
    """
    TODO: rename this function
    let g = sum_{i=1}^k {C_n_i} be written as invariant factors and let f(g) = 1 - k + sum(n_i) then:
    f(g) = V(g) in the following cases (due to citation 6):
    g is a p-group (citation 4 of citation 6)
    k <= 2 (citation 5 of citation 6)
    the first two counterexamples of f(g)=V(g) are: C_2^4+C_6 (v(g)>=11) and C_3^3+C_6 (V(g)>=13)

    TODO: this value is also a lower bound, change function to still give that result, but simply also saying if its enough or not.
    :param g:
    :return: None if there is no closed form formula, the result of said formula if there is one.
    """

    def is_pgroup(g: AbelianGroup):
        return len(set.union(*[set(primefactors(i)) for i in set(g.limit)])) == 1

    if len(g.limit) <= 2 or is_pgroup(g):
        return 1 - len(g.limit) + sum(g.limit)
    return None


@measure
def main():
    # to get an insanely detailed time analysis run: python -m cProfile main.py
    for g in group_values.keys():
        print(f"V_{memoized_calculate_v(g)} holds for {g}")


if __name__ == '__main__':
    main()
    for fname, measure in TOTAL_MEASURE.items():
        s = "\n".join(f"{key}: {measure[key]}" for key in measure.keys())
        print(f"\n\nMeasures of {fname}():\n{s}\n\n")

