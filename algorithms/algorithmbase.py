from classes.abeliangroup   import AbelianGroup
from classes.helpers.timer  import Timer
timed = Timer.measure

class VNAlgorithmBase:
    def __init__(self):
        self.name = "Base class"
        
    @timed
    def calculate_v_if_solved(self, group_to_calc: AbelianGroup):
        """
        TODO: rename this function
        let g = sum_{i=1}^k {C_n_i} be written as invariant factors and let f(g) = 1 - k + sum(n_i) then:
        f(g) = V(g) in the following cases (due to citation 6):
        g is a p-group (citation 4 of citation 6)
        k <= 2 (citation 5 of citation 6)
        the first two counterexamples of f(g)=V(g) are: C_2^4+C_6 (v(g)>=11) and C_3^3+C_6 (V(g)>=13)

        TODO: this value is also a lower bound, change function to still give that result, but simply also saying if its enough or not.
        :param g:
        :return: None if there is no closed form formula, the result of said formula if there is one.
        """

        if group_to_calc.summand_count() <= 2 or group_to_calc.is_pgroup():
            return 1 - group_to_calc.summand_count() + sum(group_to_calc.as_summand_orders())
            
        return None