from assignment.TSP import *
import numpy as np

# TODO: Test this whole thing
"""
    
"""

class TemperatureOptimizer:
    def __init__(self, cost_function, delta_cost_function, state_constructor):
        self.cost = cost_function
        self.delta_cost delta_cost_function
        self.T_iter_values = []

    
    def generate_states(self, number_of_states):
        n = self.cost.D[0]
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
                    Emaxs[l] = d_cost
                    break
        return costs, Emaxs

    def iterate_temperatures(self, T0, iter_count, Emins, Emaxs, target_acceptance_rate):
        logchi0 = np.log(target_acceptance_rate)
        T = T0
        for _ in range(iter_count):
            logchi = np.log(self.__class__.chi(T0, Emins, Emaxs))
            T *= logchi/logchi0 
            self.T_iter_values.append(T) 


    @staticmethod
    def chi(T, Emins, Emaxs):
        numerator = np.sum(np.exp(-Emaxs/T))
        denominator = np.sum(np.exp(-Emins/T))
        return numerator/denominator
