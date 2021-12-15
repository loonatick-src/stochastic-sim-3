import numpy as np

class SAMinimizer:
    def __init__(self, transition, delta_cost, cooling, state_constructor = None):
        """
        Parameters
        ----------
        transition: callable `transition(old_state)`
            return values are passed as args to delta_cost to compute
            cost of new state

        delta_cost: callable `delta_cost(old_state, *args)`
            calculates change in cost

        cooling: callable `cooling(T)`
            returns the temperature to be used in the next Markov chain
            given the current temperature `T`

        T0: float
            initial temperature

        state_constructor: callable `state_constructor(old_state, *args)`, optional
            constructs the new state from the old state and return values of
            `transition`
            If not provided, the return value of transition is assumed to be the new state
        """

        # cost function to be minimized
        self.delta_cost = delta_cost
        # transition function for Monte Carlo
        self.transition = transition
        # cooling schedule
        self.cooling = cooling

        if state_constructor is None:
            self.state_constructor = lambda old_state, new_state: new_state
        else:
            self.state_constructor = state_constructor

        self.cost_timeseries = []
        self.state = None
        self.min_cost = None
        self.min_cost_state = None


    def run(self, chain_length, T_initial, T_final, X0, cost_function):
        """
        chain_length: int
            length of the Markov chain per temperature-value

        T_initial: scalar (think Num typeclass from Haskell)
            initial temperature

        T_final: scalar 
            Smallest allowed temperature (i.e. stopping criterion
            for cooling schedule)

        X0: Any
            initial state
        """
        assert chain_length > 0, "Length of Markov chain must be a postive integer"
        assert T_final > 0, "Temperature must be postive"
        assert T_final < T_initial, "Final temperature must be lower than initial temperature"
        T = T_initial
        self.state = X0
        current_cost = cost_function(self.state)
        self.cost_timeseries.append(current_cost)
        self.min_cost = self.cost_timeseries[0]
        self.min_cost_state = X0
        k = 1
        while (T > T_final):
            # Start Markov chain for temperature T
            for i in range(chain_length):
                Xn_transition_parameters = self.transition(self.state)
                # calculate change in cost
                delta_c = self.delta_cost(self.state, *Xn_transition_parameters)
                if delta_c < 0:  # new state is lower cost
                    # construct new state
                    new_state = self.state_constructor(self.state, *Xn_transition_parameters)
                    # calculate cost of next state
                    new_cost = current_cost + delta_c
                    
                    if new_cost < self.min_cost:
                        self.min_cost = new_cost
                        self.min_cost_state = new_state
                        self.cost_timeseries.append(self.min_cost)

                    # update state and cost
                    self.state = new_state
                    current_cost = new_cost
                else:
                    boltzmann_d = np.exp(-delta_c/T)
                    u = np.random.uniform(low = 0, high = 1)
                    if boltzmann_d > u:
                        new_state = self.state_constructor(self.state, *Xn_transition_parameters)
                        current_cost += delta_c
                        self.state = new_state
                    # else do nothing
            T_colder = self.cooling(T_initial, k)
            assert T_colder < T, "Cooling schedule is actually heating schedule"
            k += 1
            T = T_colder
