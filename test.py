import unittest
from datetime import datetime
from main import memoized_calculate_v
from main import AbelianGroup as AB


class MyTestCase(unittest.TestCase):
    # groups and their values are taken from citation 6 of the paper we're looking at.
    group_values = {AB((2, )): 2,
                    AB((3, )): 3, AB((2, 2)): 3,
                    AB((4, )): 4, AB((2, 2, 2)): 4,
                    AB((5, )): 5, AB((3, 3)): 5, AB((2, 4)): 5, AB((2, 2, 2, 2)): 5,
                    AB((6, )): 6, AB((2, 2, 4)): 6,
                    AB((7, )): 7, AB((4, 4)): 7, AB((2, 6)): 7,
                    }

    # too slow for now
    # additional_group_values = {
    #     AB([2] * 5): 6,
    #     AB((3, 3, 3)): 7, AB((2, 2, 2, 4)): 7, AB([2] * 6): 7
    # }

    def test_validity(self):
        f = memoized_calculate_v
        for g, v in self.group_values.items():
            with self.subTest(function=f, group=g, value=v):
                info_string = f"\nfunction: {f.__name__}\ngroup: {g}\nresult: {v}"
                print(f"\n\nstarting: {info_string}")
                t = datetime.now()
                self.assertEqual(f(g), v, msg=info_string)
                print(f"took: {datetime.now() - t}")


if __name__ == '__main__':
    unittest.main()
