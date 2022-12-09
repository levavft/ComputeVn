from itertools              import combinations
from multiset               import Multiset, FrozenMultiset as fms
from classes.abeliangroup   import AbelianGroup, group_values
from sympy                  import primefactors

import algorithms

print("\nLoaded algorithms: ")

for alg in algorithms.get_loaded:
    print("- ", alg.name)
    
print("\n")

from classes.helpers.timer  import Timer
timed = Timer.measure

@timed
def main():
    for g in group_values.keys():
        print(f"Calculated: V({g})={memoized_calculate_v(g)}\nExpected: V({g})={group_values[g]}\n")


if __name__ == '__main__':
    main()
    for fname, measure in TOTAL_MEASURE.items():
        s = "\n".join(f"{key}: {measure[key]}" for key in measure.keys())
        print(f"\n\nMeasures of {fname}():\n{s}\n\n")

