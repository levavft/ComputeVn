from datetime import datetime
from itertools import chain, combinations


class AbelianGroup:
    def __init__(self, limit):
        self.limit = limit

    def get_elements(self, include_zero=True):
        result = [[]]
        for i in range(len(self.limit)):
            result = [[*tup, j] for tup in result for j in range(self.limit[i])]
        return (AbelianGroupElement(r, self.limit) for r in result if include_zero or not sum(r) == 0)

    def __add__(self, other):
        assert isinstance(other, AbelianGroup)
        return AbelianGroup((*self.limit, *other.limit))


class AbelianGroupElement:
    def __init__(self, value, limit):
        """
        examples for the case of the element (2, 3) in C_4+C_4
        :param value: (2, 3)
        :param limit: (4, 4)
        """
        self.value = value
        self.limit = limit

    def __interact(self, other):
        assert isinstance(other, AbelianGroupElement) or other == 0
        if other == 0:
            other = AbelianGroupElement([0] * len(self.limit), self.limit)
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

    def __repr__(self):
        return str(self.value)


def powerset(iterable):
    s = list(iterable)
    for r in range(len(s) + 1):
        for combination in combinations(s, r):
            yield combination


def generate_sums(n, m):
    """
    generates sums of m digits 0 < a < n, that sum up to a multiple of n.
    assumes n<m
    """
    assert n < m
    summand_list = [1] * (m - 1)
    index = m - 2

    while True:
        assert index == m - 2
        last_number = -sum(summand_list) % n
        if last_number >= summand_list[-1]:
            # print(*summand_list, last_number)
            yield *summand_list, last_number

        while index > -1 and summand_list[index] == n - 1:
            index -= 1

        if index == -1:
            return

        summand_list[index] += 1
        while index < len(summand_list) - 1:
            index += 1
            summand_list[index] = summand_list[index - 1]


def check_subsums(summand_list, n):
    for s in powerset(summand_list):
        if len(s) in {len(summand_list), 0}:
            continue
        if sum(s) % n == 0:
            # print(s)
            return True
    return False


def naive_cyclic_check(n, m):
    """
    assumes n<=m
    :return: True if V_m holds for C_n
    """
    assert n <= m
    for summand_list in generate_sums(n, m + 1):
        # print(summand_list)
        x = check_subsums(summand_list, n)
        # print("----------------------\n\n")
        if not x:
            print(f"V_{m} doesn't hold for n due to {summand_list}")
            return False
    return True


def main():
    # for n in range(3, 14):
        # print(f"Does V_{n} hold for C_{n}? {naive_cyclic_check(n, n)}")
    G = AbelianGroup((3, 3))
    for elem in G.get_elements(include_zero=False):
        print(elem)
    # verification time 0:00:08.163018
    # verification time 0:00:01.805139


if __name__ == '__main__':
    t = datetime.now()
    main()
    print(datetime.now() - t)
