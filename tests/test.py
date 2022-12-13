import sys

sys.path.append('../ComputeVn')

import unittest
from datetime import datetime
import algorithms
import datasets


class MyTestCase(unittest.TestCase):
    def test_validity_main_code(self):
        f = algorithms.NaiveAlgorithm.memoized_calculate_v
        for g, v in datasets.curated_small.items():
            with self.subTest(function=f, group=g, value=v):
                info_string = f"\nfunction: {f.__name__}\ngroup: {g}\nexpected: {v}"
                print(f"\nstarting: {info_string}")
                t = datetime.now()
                result = f(g)
                self.assertEqual(result, v, msg=info_string)
                print(f"result: {result}\ntook: {datetime.now() - t}")


if __name__ == '__main__':
    unittest.main()
