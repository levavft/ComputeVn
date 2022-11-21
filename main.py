from datetime import datetime
from itertools import combinations
from sympy import lcm


class AbelianGroup:
    def __init__(self, limit):
        self.limit = limit

    def elements(self, include_zero=True):
        result = [[]]
        for i in range(len(self.limit)):
            result = [[*tup, j] for tup in result for j in range(self.limit[i])]
        # print((AbelianGroupElement(r, self.limit) for r in result if include_zero or not sum(r) == 0))
        return tuple(AbelianGroupElement(r, self.limit) for r in result if include_zero or not sum(r) == 0)

    def maximal_element_order(self):
        return lcm(self.limit)

    def zero(self):
        return AbelianGroupElement([0] * len(self.limit), self.limit)

    def __add__(self, other):
        assert isinstance(other, AbelianGroup)
        return AbelianGroup((*self.limit, *other.limit))

    def __repr__(self):
        return f"<{self.limit}>"


class AbelianGroupElement:
    def __init__(self, value, limit):
        """
        examples for the case of the element (2, 3) in C_4+C_4
        :param value: (2, 3)
        :param limit: (4, 4)
        """
        self.value = tuple(value)
        self.limit = tuple(limit)

    def __zero_like(self):
        return AbelianGroupElement([0] * len(self.limit), self.limit)

    def __interact(self, other):
        assert isinstance(other, AbelianGroupElement) or other == 0
        if other == 0:
            other = self.__zero_like()
        assert self.limit == other.limit
        return other

    def __add__(self, other):
        other = self.__interact(other)
        return AbelianGroupElement(((self.value[i] + other.value[i]) % self.limit[i] for i in range(len(self.value))),
                                   self.limit)

    def __sub__(self, other):
        other = self.__interact(other)
        return AbelianGroupElement(((self.value[i] - other.value[i]) % self.limit[i] for i in range(len(self.value))),
                                   self.limit)

    def __neg__(self):
        return self.__zero_like() - self

    def __eq__(self, other):
        other = self.__interact(other)
        return self.value == other.value

    def __repr__(self):
        return str(self.value)


def powerset(iterable):
    s = list(iterable)
    for r in range(len(s) + 1):
        for combination in combinations(s, r):
            yield combination


def generate_increasing_lexicographical(l, r, length):
    r"""
    Generate all numbers of form a_1a_2...a_n where if i<j: a_i <= a_j
    It might be a good idea to avoid the recursion here. We'll see if it creates problems.
    :param l: a_i \in {l,l + 1,...,r - 1}
    :param r: a_i \in {l,l + 1,...,r - 1}
    :param length: n
    :return:
    """
    assert r > l
    if length == 1:
        for i in range(l, r):
            yield [i]
    for i in range(l, r):
        for sub_arr in generate_increasing_lexicographical(i, r, length=length - 1):
            yield [i, *sub_arr]
            # we would like to get "feedback" from our yielded number here, if it says "sub sum found!" -->
            # we can break this inner array. here's a good thing to read (we would probably go for YieldReceive):
            # https://stackoverflow.com/questions/50913292/python-create-an-iterator-generator-with-feedback


def generate_sums(group, m):
    """
    generates sums of m digits 0 < a < n, that sum up to a multiple of n.
    assumes n < m
    """
    assert isinstance(group, AbelianGroup)
    assert group.maximal_element_order() < m
    summand_index_list = [0] * (m - 1)
    elements = group.elements(include_zero=False)
    assert isinstance(elements, tuple)
    index = m - 2
    n = len(elements)

    while True:
        assert index == m - 2
        last_element = -sum((elements[i] for i in summand_index_list), start=group.zero())
        last_element_index = None
        if last_element != 0:
            last_element_index = elements.index(last_element)
        if last_element != 0 and last_element_index >= summand_index_list[-1]:
            # print(*summand_index_list, last_element)
            yield tuple(elements[i] for i in (*summand_index_list, last_element_index))

        while index > -1 and summand_index_list[index] == n - 1:
            index -= 1

        if index == -1:
            return

        summand_index_list[index] += 1
        while index < len(summand_index_list) - 1:
            index += 1
            summand_index_list[index] = summand_index_list[index - 1]


def check_sub_sums(summand_list, group):
    for s in powerset(summand_list):
        if len(s) in {len(summand_list), 0}:
            continue
        if sum(s, start=group.zero()) == group.zero():
            # print(s)
            return True
    return False


def naive_group_check(group, m):
    """
    assumes n<=m
    :return: True if V_m holds for C_n
    """
    assert group.maximal_element_order() <= m
    for summand_list in generate_sums(group, m + 1):
        # print(summand_list)
        x = check_sub_sums(summand_list, group)
        # print("----------------------\n\n")
        if not x:
            # print(f"V_{m - 1} doesn't hold for {group} due to {summand_list}")
            return False
    return True


def calculate_v(group, max_tries=10):
    assert isinstance(group, AbelianGroup)
    meo = group.maximal_element_order()
    for m in range(meo + 1, meo + max_tries + 1):
        result = naive_group_check(group, m)
        if result:
            return m - 1


def main():
    groups = (AbelianGroup((2, 2, 3)),)
    for g in groups:
        print(f"V_{calculate_v(g)} holds for {g}")
        print()
        print()

    # hint - a group with about 25 elements can take around 2 minutes to check V_6.
    # with n elements, the ratio between calculating V_m and V_m+1 is about ((m+2)/(m+1))^n soooo, yea, painful.


if __name__ == '__main__':
    t = datetime.now()
    main()
    print(datetime.now() - t)
