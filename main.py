from classes.helpers.timer  import Timer
from classes.abeliangroup   import AbelianGroup

import algorithms
import datasets

timed = Timer.measure
##################################################################

print("\nLoaded algorithms: ")

for alg in algorithms.get_loaded:
    print("- ", alg.name)
    
print("\n")

@timed
def main():

    dataset = datasets.curated_small

    for g in dataset.keys():
        print(f"Calculated: V({g})={algorithms.NaiveAlgorithm.memoized_calculate_v(g)}\nExpected: V({g})={dataset[g]}\n")


if __name__ == '__main__':
    main()
    for fname, measure in Timer.TOTAL_MEASURE.items():
        s = "\n".join(f"{key}: {measure[key]}" for key in measure.keys())
        print(f"\n\nMeasures of {fname}():\n{s}\n\n")
