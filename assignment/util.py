import numpy as np
from os.path import exists
from os import mkdir
from os import listdir
from assignment.TSP import cost_function_factory

SAVEDIR = "save_data"
PLOTDIR = "plots"
DATADIR = "TSP-Configurations"

DIRS = [SAVEDIR, PLOTDIR, DATADIR]

def parse_str_to_int(s):
    numeric_chars = filter(lambda s: s.isnumeric(), s)
    num_str_repr = ''.join(numeric_chars)
    num = int(num_str_repr)
    return num

def savepath(filename):
    return SAVEDIR + f"/{filename}"

def plot_savepath(filename):
    return PLOTDIR + f"/{filename}"

def data_path(filename):
    return DATADIR + f"/{filename}"

def generate_rngs(count, seed = 0xc0ffee):
    ss = np.random.SeedSequence(seed)
    child_seeds = ss.spawn(count)
    streams = [np.random.default_rng(s) for s in child_seeds]
    return streams

for d in DIRS:
    if not exists(d):
        mkdir(d)

TSP_FILES = listdir(DATADIR)
# LOL
OPT_TOUR_FILES = sorted(filter(lambda path: "opt.tour" in path, TSP_FILES), key = parse_str_to_int)
ADJ_FILES = list(filter(lambda path: ".adj" in path, TSP_FILES))

def import_tsp_file(tsp_txt):
    
    filename = tsp_txt
    filepath = data_path(filename)
    
    cities=[]
    
    with open(filepath, "r") as f:
        contents = f.read()
        file_as_list = contents.splitlines()[6:]

        for i, line in enumerate(file_as_list):
            if line.strip() == "EOF":
                break
                
            a_list = line.split()
            map_object = map(float, a_list)
            list_of_integers = list(map_object)
            cities.append(list_of_integers)
            

    return cities

def first(x):
    return x[0]

def second(x):
    return x[1]

def take2(x):
    return first(x) , second(x)

def take2_arr(x):
    return np.array(take2(x))

def sq(x):
    return np.power(x,2)

def l2normsq(x):
    return np.sum(sq(x))

def l2norm(x):
    return np.sqrt(l2normsq(x))

def distance(x1, x2):
    displacement = x1 - x2
    dist = l2norm(displacement)
    return dist

def symmetric_p(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i+1, n):
            if a[i][j] != a[j][i]:
                return False
    return True

def adj_matrix(cities):
    n = len(cities)
    a_mat = np.empty((n,n))
    for i in range(n):
        a_mat[i][i] = 0.0

    for i in range(n):
        for j in range(i+1,n):
            xy1 = take2_arr(cities[i][1:])
            xy2 = take2_arr(cities[j][1:])
            weight = distance(xy1, xy2)
            a_mat[i][j] = a_mat[j][i] = weight

    return a_mat


def save_adj_matrix(filename):
    cities = import_tsp_file(filename)
    a_mat = adj_matrix(cities)
    npz_filename = data_path(filename) + ".adj"
    np.savez(npz_filename, a_mat)
    

def load_adj_matrix(filename):
    npz_filename = data_path(filename)
    save_data = np.load(npz_filename)
    return save_data['arr_0']

def load_all_adj_matrices():
    filenames = listdir(DATADIR)
    adj_ext_rev = "adj.npz"[::-1]
    matrices = []
    for fname in filenames:
        if fname[-1:-8:-1] == adj_ext_rev:
            matrices.append(load_adj_matrix(fname))
    return matrices



def read_tour(filename):
    filepath = data_path(filename)
    with open(filepath, "r") as f:
        lines = f.readlines()
        optimal_solution = np.float64(lines[2].strip().split()[-1][1:-1])
        relevant_lines = lines[5:-1]
        typed_data = np.array(list(map(np.int32, relevant_lines)), dtype = np.int32)
        typed_data -= 1
        typed_data
        return optimal_solution, typed_data


ADJ_MATRICES = load_all_adj_matrices()
COST_FUNCTION_PAIRS = [cost_function_factory(matrix) for matrix in ADJ_MATRICES]
COST_FUNCTIONS = list(map(first, COST_FUNCTION_PAIRS))
DELTA_COST_FUNCTIONS = list(map(second, COST_FUNCTION_PAIRS))


if __name__ == '__main__':
    filenames = listdir(DATADIR)
    for fname in filenames:
        if fname[-1:-8:-1] == "txt.pst":
            save_adj_matrix(fname)
    print("Adjacency matrices saved. Hopefully.")
