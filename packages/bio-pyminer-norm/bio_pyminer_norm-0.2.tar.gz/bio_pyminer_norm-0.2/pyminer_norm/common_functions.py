"""
Commonly used functions for PyMINEr-norm
"""
import os
import pickle
import numpy as np
from subprocess import check_call, Popen, PIPE
from scipy.sparse import csc_matrix, lil_matrix
import h5py
#####################################################

def cp(file1,file2):
    with open(file1, 'rb') as f_in:
        with open(file2, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return()


def rm(rm_file):
    if os.path.isfile(rm_file):
        os.remove(rm_file)
    else:
        print('WARNING:',rm_file,"doesn't exist, couldn't remove it")
    return()


def run_cmd(in_message, com=True, stdout=None):

    print('\n', " ".join(in_message), '\n')
    if stdout:
        with open(stdout, 'w') as out:
            process = Popen(in_message, stdout=PIPE)
            while True:
                line = process.stdout.readline().decode("utf-8")
                out.write(line)
                if line == '' and process.poll() is not None:
                    break
    if com:
        Popen(in_message).communicate()
    else:
        check_call(in_message)


def read_file(file_name, lines_or_raw='lines', quiet=False):
    """ basic function library """
    print("reading file " + file_name)
    lines = None
    if not quiet:
        print('reading', file_name)
    with open(file_name, 'r') as file_handle:
        if lines_or_raw == 'lines':
            lines = file_handle.readlines()
            for i, line in enumerate(lines):
                lines[i] = line.strip('\n')
        elif lines_or_raw == 'raw':
            lines = file_handle.read()
    return lines


def make_file(contents, path):
    with open(path, 'w') as file_handle:
        if isinstance(contents, list):
            file_handle.writelines(contents)
        elif isinstance(contents, str):
            file_handle.write(contents)


def flatten_2D_table(table, delim):
    # print(type(table))
    if str(type(table)) == "<class 'numpy.ndarray'>":
        out = []
        for i, row in enumerate(table):
            out.append([])
            for j, cell in enumerate(row):
                try:
                    str(cell)
                except ValueError:
                    print(cell)
                else:
                    out[i].append(str(cell))
            out[i] = delim.join(out[i]) + '\n'
        return out
    else:
        for i, row in enumerate(table):
            for j, cell in enumerate(row):
                try:
                    str(cell)
                except ValueError:
                    print(cell)
                else:
                    table[i][j] = str(cell)
            table[i] = delim.join(row) + '\n'
        return table


def strip_split(line, delim='\t'):
    return line.strip('\n').split(delim)


def make_table(lines, delim, range_min=0):
    for i in range(range_min, len(lines)):
        lines[i] = lines[i].strip()
        lines[i] = lines[i].split(delim)
        for j in range(range_min, len(lines[i])):
            try:
                float(lines[i][j])
            except ValueError:
                lines[i][j] = lines[i][j].replace('"', '')
            else:
                lines[i][j] = float(lines[i][j])
    return lines


def get_file_path(in_path):
    in_path = in_path.split('/')
    in_path = in_path[:-1]
    in_path = '/'.join(in_path)
    return in_path + '/'


def read_table(file, sep='\t'):
    return make_table(read_file(file, 'lines'), sep)


def write_table(table, out_file, sep='\t'):
    make_file(flatten_2D_table(table, sep), out_file)


def import_dict(file_handle):
    file_handle = open(file_handle, 'rb')
    data = pickle.load(file_handle)
    file_handle.close()
    return data


def save_dict(data, path):
    file_handle = open(path, 'wb')
    pickle.dump(data, file_handle)
    file_handle.close()


def process_dir(in_dir):
    ## process the output dir
    if in_dir[-1]!='/':
        in_dir+='/'
    if not os.path.isdir(in_dir):
        os.makedirs(in_dir)
    return(in_dir)



##################################################################
############### some ray specific functions ######################
def get_num_rows_from_dict_lists(dict_list):
    ## goes through all of the indices & returns the number of dims
    row_dims = 0
    for temp_dict in dict_list:
        for temp_key in list(temp_dict.keys()):
            #print(temp_key)
            if temp_key > row_dims:
                row_dims = temp_key
    return(row_dims+1)


def get_num_cols_from_dict_lists(dict_list):
    ## first get the dimentions
    first_key = list(dict_list[0].keys())[0]
    first = dict_list[0][first_key]
    if type(first) == list:
        col_dims = len(first)
    elif type(first) == np.ndarray:
        col_dims = first.shape[0]
    else:
        col_dims = 1
    return(col_dims)


def ray_dicts_to_array(dict_list,dicts_are_cols = False):
    row_dims = get_num_rows_from_dict_lists(dict_list)
    col_dims = get_num_cols_from_dict_lists(dict_list)
    out_array = np.zeros((row_dims, col_dims))
    print(out_array)
    for temp_dict in dict_list:
        for idx, value in temp_dict.items():
            #print(idx)
            #print(value)
            out_array[idx] = value
    if dicts_are_cols:
        return(np.transpose(out_array))
    else:
        return(out_array)


def get_indices(threads, num_genes):
    indices_list = []
    for t in range(threads):
        indices_list.append([])
    temp_idx = 0
    while temp_idx < num_genes:
        for t in range(threads):
            if temp_idx < num_genes:
                indices_list[t].append(temp_idx)
                temp_idx += 1
    return(indices_list)



def get_contiguous_indices(threads, num_genes):
    old_format_indices = get_indices(threads, num_genes)
    new_indices = []
    for t in range(threads):
        new_indices.append([])
    cur_idx=0
    for t in range(threads):
        while len(new_indices[t]) <= len(old_format_indices[t]) and cur_idx<num_genes:
            new_indices[t].append(cur_idx)
            cur_idx+=1
    return(new_indices)



def ray_get_indices_from_list(threads, original_idx_list):
    indices_list = []
    for t in range(threads):
        indices_list.append([])
    temp_idx = 0
    while temp_idx < len(original_idx_list):
        for t in range(threads):
            if temp_idx < len(original_idx_list):
                indices_list[t].append(original_idx_list[temp_idx])
                temp_idx += 1
    return(indices_list)

##########################################################


def read_cz_h5(in_file, load_binary=False):
    h5f = h5py.File(in_file , 'r')
    if 'X' not in h5f:
        print("couldn't find the data in the cz h5 file")
    if 'shape' in dir(h5f['X']):
        in_mat= lil_matrix(h5f['X'])
    elif 'keys' in dir(h5f['X']):
        if ('data' in h5f['X']) and ('indices' in h5f['X'])  and ('indptr' in h5f['X']):
            if not load_binary:
                in_mat= csc_matrix((h5f['X']['data'], h5f['X']['indices'], h5f['X']['indptr']))
            else:
                data_vect=np.ones(h5f['X']['data'].shape)
                in_mat= csc_matrix((data_vect, h5f['X']['indices'], h5f['X']['indptr']))
    ## read the genes
    if "shape" in dir(h5f['var']):
        genes = [entry[0] for entry in h5f['var']]
    ## read the cells
    if "shape" in dir(h5f['obs']):
        cells = ['variable'] + [entry[0] for entry in h5f['obs']]
    h5f.close()
    return(in_mat, genes, cells)

