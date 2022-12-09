from classes.abeliangroup import AbelianGroup as AB

all =   {
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
                            
curated_small = {   
                AB((2, )): 2,
                AB((3, )): 3, AB((2, 2)): 3,
                AB((4, )): 4, AB((2, 2, 2)): 4,
                AB((5, )): 5, AB((3, 3)): 5, AB((2, 4)): 5, AB((2, 2, 2, 2)): 5,
                AB((6, )): 6, AB((2, 2, 4)): 6, AB(tuple([2] * 5)): 6,
                AB((7, )): 7, AB((4, 4)): 7, AB((2, 6)): 7,
                }