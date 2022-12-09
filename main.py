from itertools              import combinations
from multiset               import Multiset, FrozenMultiset as fms
from sympy                  import primefactors

from classes.helpers.timer  import Timer
from classes.abeliangroup   import AbelianGroup
import algorithms

timed = Timer.measure

print("\nLoaded algorithms: ")

for alg in algorithms.get_loaded:
    print("- ", alg.name)
    
print("\n")

AB = AbelianGroup
known_group_vn_kvpairs =    {
                            AB((2, )): 2,
                            AB((3, )): 3, AB((2, 2)): 3,
                            AB((4, )): 4, AB((2, 2, 2)): 4,
                            AB((5, )): 5, AB((3, 3)): 5, AB((2, 4)): 5, AB((2, 2, 2, 2)): 5,
                            AB((6, )): 6, AB((2, 2, 4)): 6, AB(tuple([2] * 5)): 6,
                            AB((7, )): 7, AB((4, 4)): 7, AB((2, 6)): 7, AB((3, 3, 3)): 7, AB((2, 2, 2, 4)): 7, AB(tuple([2] * 6)): 7,
                            AB((8, )): 8, AB((3, 6)): 8, AB((2, 4, 4)): 8, AB((2, 2, 6)): 8, AB(tuple([2] * 4 + [4])): 8, AB(tuple([2] * 7)): 8,
                            AB((9, )): 9, AB((2, 8)): 9, AB((5, 5)): 9, AB((2, 2, 4, 4)): 9, AB(tuple([3] * 4)): 9, AB((2, 2, 2, 6)): 9, AB(tuple([2] * 5 + [4])): 9, AB(tuple([2] * 8)): 9,
                            AB((10, )): 10, AB((2, 2, 8)): 10, AB((4, 4, 4)): 10, AB((3, 3, 6)): 10, AB((2, 2, 2, 4, 4)): 10, AB(tuple([2] * 6 + [4])): 10, AB(tuple([2] * 9)): 10,
                            }

@timed
def main():
    for g in group_values.keys():
        print(f"Calculated: V({g})={algorithms.NaiveAlgorithm.memoized_calculate_v(g)}\nExpected: V({g})={group_values[g]}\n")


if __name__ == '__main__':
    main()
    for fname, measure in Timer.TOTAL_MEASURE.items():
        s = "\n".join(f"{key}: {measure[key]}" for key in measure.keys())
        print(f"\n\nMeasures of {fname}():\n{s}\n\n")

