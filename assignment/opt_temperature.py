from assignment.lib import *
import numpy as np

# FIXME
# Doesn't appear to be working as intended. Debug later if life permits
"""
    
"""

class TemperatureOptimizer:
    def __init__(self, cost_function, delta_cost_function):
        self.cost = cost_function
        self.delta_cost = delta_cost_function
        self.T_iter_values = []

    
    def generate_states(self, number_of_states):
        n = self.cost.D.shape[0]
        states_list = []
        for _ in range(number_of_states):
            state = np.random.permutation(n)
            states_list.append(state)
        costs = np.array([self.cost(state) for state in states_list])
        return states_list, costs


    def generate_positive_transitions(self, states_list, costs):
        Emaxs = np.empty(len(costs))
        for l,state in enumerate(states_list):
            while (True):
                # will not terminate with probability zero
                i,k = random_two_opt_transition(state)
                d_cost = self.delta_cost(state, i, k)
                if d_cost > 0:
                    new_cost = costs[l] + d_cost
                    Emaxs[l] = new_cost
                    break
        return costs, Emaxs


    def iterate_temperatures(self, T0, Emins, Emaxs, target_acceptance_rate, eps = 0.1, max_iter = 10**5, p = 1):
        # TODO: verify
        chi0 = target_acceptance_rate
        logchi0 = np.log(target_acceptance_rate)
        T = T0
        i = 0
        chi_n = self.__class__.chi(T, Emins, Emaxs)
        while (i < max_iter and np.abs(chi0 - chi_n) > eps):
            logchi = np.log(chi_n)
            T *= np.power(logchi/logchi0, p)
            self.T_iter_values.append(T) 
            chi_n = self.__class__.chi(T, Emins, Emaxs)


    def iterate_from_scratch(self, S, T0, target_acceptance_rate, eps = 0.1, max_iter = 10**5):
        states_list, Emins = self.generate_states(S)
        Emins, Emaxs = self.generate_positive_transitions(states_list, Emins)
        self.iterate_temperatures(T0, Emins, Emaxs, target_acceptance_rate, eps = eps, max_iter = max_iter)


    @staticmethod
    def chi(T, Emins, Emaxs):
        # TODO: Verify
        numerator = np.sum(np.exp(-Emaxs/T))
        denominator = np.sum(np.exp(-Emins/T))
        return numerator/denominator


def search_target_temperature(chi0, sa_system, T0 = 1000, chain_length = 1000):
    raise NotImplementedError
    X0 = SAMinimizer.generate_random_state()







"""
if __name__ == '__main__':
    cost_func, dcost_func = COST_FUNCTION_PAIRS[0]
    temp_opter = TemperatureOptimizer(cost_func, dcost_func)
    S = 100
    states_list, Emins = temp_opter.generate_states(100)
    Emins, Emaxs = temp_opter.generate_positive_transitions(states_list, Emins)
    T0 = 100.0
    iter_count = 100 
    temp_opter.iterate_temperatures(T0, iter_count, Emins, Emaxs, 0.8)
    print(temp_opter.T_iter_values)

"""
