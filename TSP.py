import numpy as np

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
        for i in range(len(self.D)):
            cost += self.D[i][route[i]]
        return cost


class TSPDeltaCost:
    def __init__(self, adj_matrix: np.ndarray):
        assert adj_matrix.shape[0] == adj_matrix.shape[1]
        self.D = adj_matrix

    def __call__(route, i, k):
        delta_c = 0.0
        delta_c -= self.D[route[i-1]][route[i]]
        delta_c -= self.D[route[k]][route[k+1]]
        delta_c += self.D[route[i-1]][route[k+1]]
        delta_c += self.D[route[i]][route[k]]
        return delta_c


def random_two_opt_transition(state):
    n = len(state)
    assert n > 4, "What is this pussy-ass TSP?"
    lim = (1,n-1)
    i = np.random.randint(*lim)
    j = np.random.randint(*lim)
    while (j == i):
        j = np.random.randint(*lim)
    return i,j
