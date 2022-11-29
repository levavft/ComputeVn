from abeliangroup import *

def V(C: AbelianGroup):
    return 1 - len(C.limit) + sum(C.limit)
    
if __name__ == "__main__":
    for (g, v) in group_values.items():
        print(f"Group: {g}\n\tExpected V: {v}\n\tFormula V: {V(g)}\n");
