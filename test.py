import unittest
from datetime import datetime, timedelta
from main import calculate_v, AbelianGroup


class MyTestCase(unittest.TestCase):
    # the tests here are based on the results of the first version of the code. Replace them with values from papers.
    # For now version names will just appear in commit names.
    groups = (*[AbelianGroup((i,)) for i in range(2, 11)],
              *[AbelianGroup((i, j)) for i in range(2, 5) for j in range(i, 5)],
              AbelianGroup((2, 2, 2)), AbelianGroup((2, 2, 3)))
    results = (*[i for i in range(2, 11)], 2, 6, 4, 4, 12, 6, 3, 6)
    times = [timedelta(0), timedelta(0), timedelta(0), timedelta(0), timedelta(microseconds=31660),
             timedelta(microseconds=94162), timedelta(microseconds=329380),
             timedelta(seconds=1, microseconds=405246), timedelta(seconds=5, microseconds=256897), timedelta(0),
             timedelta(microseconds=16058), timedelta(microseconds=15737), timedelta(microseconds=46975),
             timedelta(seconds=86, microseconds=734311), timedelta(seconds=7, microseconds=27984), timedelta(0),
             timedelta(seconds=1, microseconds=99336)]

    def test(self):
        for g, r, tt in zip(self.groups, self.results, self.times):
            with self.subTest(group=g, result=r, time=str(tt)):
                t = datetime.now()
                self.assertEqual(calculate_v(g), r)
                # time tends to vary quite a bit between two runs, might also vary between computers.
                self.assertLessEqual(datetime.now() - t, tt * 1.5 + timedelta(microseconds=10**4),
                                     msg=f"\ngroup: {g}\nresult: {r}\ntime: {tt}")


if __name__ == '__main__':
    unittest.main()
