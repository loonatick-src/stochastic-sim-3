import numpy as np
import unittest

def Lin2opt_inplace(route, i, k):
    """Assumes route does not impl `Copy`, iygwim"""
    route[i:k+1] = route[k:i-1:-1]

def Lin2opt(route, i, k):
    new_route = np.copy(route)
    new_route[i:k+1] = route[k:i-1:-1]
    return new_route


class TSPCost:
    """
    Assumes planar graph with edge-weights equal to Euclidean
    distance between node embeddings
    """
    def __init__(self, adj_matrix: np.ndarray):
        """Assumes adj_matrix is symmetric if it is square"""
        assert adj_matrix.shape[0] == adj_matrix.shape[1], "Adjacency matrix is not square"
        self.D = adj_matrix

    def __call__(self, route):
        """Computes cost of route"""
        cost = 0.0
        n = len(self.D)
        for i in range(n):
            cost += self.D[route[i]][route[(i+1)%n]]
        return cost


class TSPDeltaCost:
    def __init__(self, adj_matrix: np.ndarray):
        assert adj_matrix.shape[0] == adj_matrix.shape[1]
        self.D = adj_matrix

    def __call__(self, route, i, k):
        """
        Comutes the change in cost of the route when the
        transformation is a Lin-2-opt
        """
        delta_c = 0.0
        # sever connection between i and i's predecessor
        delta_c -= self.D[route[i-1]][route[i]]
        # sever connection between k and k's successor
        delta_c -= self.D[route[k]][route[k+1]]
        # form connection between i's predecessor and k
        delta_c += self.D[route[i-1]][route[k]]
        # form connection between k's successor and i
        delta_c += self.D[route[i]][route[k+1]]
        return delta_c

def cost_function_factory(adj_matrix):
    assert adj_matrix.shape[0] == adj_matrix.shape[1]
    cost_func = TSPCost(adj_matrix)
    dcost_func = TSPDeltaCost(adj_matrix)
    return cost_func, dcost_func


def random_two_opt_transition(state):
    n = len(state)
    assert n > 4, "What is this pussy-ass TSP?"
    i = np.random.randint(1,n-1)
    j = np.random.randint(1,n-1)
    while (j == i):
        j = np.random.randint(1,n-1)
    return i,j

class TestCost(unittest.TestCase):
    def test_cost_51(self):
        raise NotImplementedError


if __name__ == '__main__':
    raise NotImplementedError("Test cases not implemented")

