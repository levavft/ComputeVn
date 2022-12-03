import unittest
from datetime import datetime
from main import memoized_calculate_v
from abeliangroup import group_values


class MyTestCase(unittest.TestCase):
    def test_validity_main_code(self):
        f = memoized_calculate_v
        for g, v in group_values.items():
            with self.subTest(function=f, group=g, value=v):
                info_string = f"\nfunction: {f.__name__}\ngroup: {g}\nexpected: {v}"
                print(f"\nstarting: {info_string}")
                t = datetime.now()
                result = f(g)
                self.assertEqual(result, v, msg=info_string)
                print(f"result: {result}\ntook: {datetime.now() - t}")


if __name__ == '__main__':
    unittest.main()
