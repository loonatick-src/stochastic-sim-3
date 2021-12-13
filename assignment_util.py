import numpy as np
from os.path import exists
from os import mkdir
from os import listdir

SAVEDIR = "save_data"
PLOTDIR = "plots"
DATADIR = "TSP-Configurations"

DIRS = [SAVEDIR, PLOTDIR, DATADIR]


def savepath(filename):
    return SAVEDIR + f"/{filename}"

def plot_savepath(filename):
    return PLOTDIR + f"/{filename}"

def data_path(filename):
    return DATADIR + f"/{filename}"

for d in DIRS:
    if not exists(d):
        mkdir(d)


def import_tsp_file(tsp_txt):
    
    filename = tsp_txt
    filepath = data_path(filename)
    
    cities=[]
    
    with open(filepath) as f:
        contents = f.read()
        file_as_list = contents.splitlines()[6:]

        for i, line in enumerate(file_as_list):
            print(line)
            if line.strip() == "EOF":
                break
                
            a_list = line.split()
            map_object = map(float, a_list)
            list_of_integers = list(map_object)
            cities.append(list_of_integers)
            

    return cities


def distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2)**2))


def adj_matrix(cities):
    n = len(cities)
    a_mat = np.empty((n,n))
    for i in range(n):
        for j in range(n):
            a_mat[i][j] = distance(np.array([cities[i][1], cities[i][2]]), np.array([cities[j][1], cities[j][2]]))
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


if __name__ == '__main__':
    filenames = listdir(DATADIR)
    for fname in filenames:
        if fname[-1:-8:-1] == "txt.pst":
            save_adj_matrix(fname)
    print("Adjacency matrices saved. Hopefully.")
