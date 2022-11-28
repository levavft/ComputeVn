import unittest
from datetime import datetime
from main import memoized_calculate_v
from abeliangroup import group_values


class MyTestCase(unittest.TestCase):
    def test_validity(self):
        f = memoized_calculate_v
        for g, v in group_values.items():
            with self.subTest(function=f, group=g, value=v):
                info_string = f"\nfunction: {f.__name__}\ngroup: {g}\nresult: {v}"
                print(f"\n\nstarting: {info_string}")
                t = datetime.now()
                self.assertEqual(f(g), v, msg=info_string)
                print(f"took: {datetime.now() - t}")


if __name__ == '__main__':
    unittest.main()
