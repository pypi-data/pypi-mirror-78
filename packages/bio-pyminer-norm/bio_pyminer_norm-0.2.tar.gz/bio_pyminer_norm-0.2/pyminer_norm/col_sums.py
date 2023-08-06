# pylint: disable=C0411,C0413
import sys
import os
import numpy as np
import argparse
import shutil

import matplotlib as mpl
mpl.use('Agg')

from scipy import sparse
import seaborn as sns
import h5py

from pyminer_norm.common_functions import get_file_path, make_file, read_table, run_cmd, read_file, write_table


def parse_arguments(parser=None):
    """ Define the arguments available on the command line."""
    if not parser:
        parser = argparse.ArgumentParser()

    parser.add_argument("-input_file", "-i", "-infile",
                        help="the input matrix which needs to be transformed")

    parser.add_argument('-count_non_zero', '-count',
                        help="if we should just count the non-zeros for each column instead of summing the columns.",
                        action='store_true',
                        default=False)

    parser.add_argument('-cell_ranger', '-cr',
                        help="If this is a cell ranger hdf5 file.",
                        action='store_true',
                        default=False)

    parser.add_argument('-hdf5', '-h5',
                        help="If this is a PyMINEr hdf5 file.",
                        action='store_true',
                        default=False)

    parser.add_argument("-ID_list", "-ids",
                        help='If we are using an hdf5 file, give the row-wise IDs in this new line delimeted file',
                        type=str)

    parser.add_argument("-columns", "-cols",
                        help='If we are using an hdf5 file, give the column-wise IDs in this new line delimeted file',
                        type=str)

    parser.add_argument("-filter", "-range", '-f', '-r',
                        help="the range to keep if you want to filter the file. Should be in the format of: "
                             "lower_bound,upper_bound. If only one value is given it will be considered the "
                             "lower bound")

    parser.add_argument('-remove_zero', '-rmz',
                        help="If you want to remove the sum-zero genes as well",
                        action='store_true',
                        default=False)

    parser.add_argument('-norm_col',
                        help="normalize the columns",
                        action="store_true")

    parser.add_argument('-mult_by',
                        help="what to multiply by in the case of col norm",
                        default=1e6,
                        type=float)

    args = parser.parse_args()
    return args


def untuple(in_tup):
    """ A convenience function, used to wrap a tuple-to-list function used in a map call """
    return list(in_tup)


def bytes_to_str(in_bytes):
    """ A wrapper for byte string conversion to utf-8 (standard) strings."""
    return in_bytes.decode("utf-8")


def main():
    """ Warpper to run the code in this file from the command line."""
    args = parse_arguments()

    type_of_analysis = 'count' if args.count_non_zero else 'sum'

    calculate_col_sum(input_file=args.input_file,
                      type_of_analysis=type_of_analysis,
                      cell_ranger=args.cell_ranger,
                      hdf5=args.hdf5,
                      id_list_file=args.ID_list,
                      columns=args.columns,
                      remove_zero=args.remove_zero,
                      norm_col=args.norm_col,
                      mult_by=args.mult_by,
                      filter_data=args.filter)


def calculate_col_sum(input_file, type_of_analysis='sum', cell_ranger=False, hdf5=False,
                      id_list_file=None, columns=None, remove_zero=False, norm_col=False,
                      mult_by=1e6, filter_data=None):

    if type_of_analysis not in ['sum', 'count']:
        print("doing:",type_of_analysis)
        raise ValueError("type_of_analysis must be either \'sum\' or \'count\'")

    out_dir = get_file_path(input_file)
    print(out_dir)
    ids = None
    in_mat_num = None
    id_list = None

    if not cell_ranger and not hdf5:
        in_mat = read_table(input_file)
        print("full table shape:")
        print("rows:",len(in_mat),"cols:",len(in_mat[0]))
        print("row2 cols:",len(in_mat[1]))
        col_sum_table = np.transpose(np.array([in_mat[0][1:]]))
        # print(col_sum_table)
        ids = in_mat[0]
        del in_mat[0]
        in_mat_num = np.zeros((len(in_mat), len(in_mat[0]) - 1), dtype=float)

        # in_mat_num = np.array(in_mat[1:,1:],dtype = float)

        for i in range(1, len(in_mat)):
            in_mat_num[i, :] = in_mat[i][1:]

        print("in_mat_num.shape",in_mat_num.shape)
    elif cell_ranger:

        in_mat_file = h5py.File(input_file, 'r')
        ref = list(in_mat_file.keys())[0]

        in_mat_num = sparse.csc_matrix((in_mat_file[ref]['data'],
                                        in_mat_file[ref]['indices'],
                                        in_mat_file[ref]['indptr']),
                                       shape=(in_mat_file[ref]['shape'][0], in_mat_file[ref]['shape'][1]))
        ids = np.array(in_mat_file[ref]['barcodes'])
        ids = ids.tolist()
        ids = list(map(bytes_to_str, ids))
        print('ids:')
        print(ids[:3], '...')
        id_list = list(map(bytes_to_str, in_mat_file[ref]["genes"]))
    elif hdf5:
        id_list = read_file(id_list_file, 'lines')
        ids = read_file(columns, 'lines')
        print('making a maliable hdf5 file to preserve the original data')
        shutil.copyfile(input_file, input_file + '_copy')

        print('reading in hdf5 file')
        infile_path = input_file + '_copy'
        h5f = h5py.File(infile_path, 'r+')
        in_mat_num = h5f["infile"]
    if type_of_analysis == 'count' and not cell_ranger:
        print("converting to counts")
        in_mat_num[in_mat_num[:,:] != 0] = 1
        # for i in range(in_mat_num.shape[1]):
        #     if (i%1000)==0 and i != 0:
        #         print("\t",i)
        #     temp_vect = in_mat_num[:,i]
        #     temp_vect[temp_vect != 0] = 1
        #     in_mat_num[:,i] = temp_vect
    col_sums = np.sum(in_mat_num, axis=0)
    # print(col_sums)
    print("colsums shape:",np.shape(col_sums))
    if not cell_ranger or hdf5:
        print('len IDs:', len(ids))
        colsum_t = np.transpose(np.array([list(col_sums)]))
        id_vect = np.transpose(np.array([list(ids[1:])]))
        print("colsum_t shape:",colsum_t.shape)
        print("id_vect shape:",id_vect.shape)
        col_sum_table = np.concatenate((id_vect, colsum_t), axis=1)
        col_sum_table = col_sum_table.tolist()
    else:
        col_sums = np.array(col_sums.tolist()[0])
        print(col_sums[:2])
        log_col_sums = np.log10(col_sums + 1)
        print(len(ids))
        col_sum_table = list(zip(ids, col_sums, log_col_sums))
        col_sum_table = list(map(untuple, col_sum_table))
        print(col_sum_table[0])
    col_sum_table_copy = [['sample', type_of_analysis]]
    for i, row in enumerate(col_sum_table):
        col_sum_table_copy.append(row)
    write_table(col_sum_table_copy, os.path.splitext(input_file)[0] + '_col_' + type_of_analysis + '.txt')
    plt = sns.violinplot(col_sums)
    fig = plt.get_figure()
    fig.savefig(os.path.splitext(input_file)[0] + '_col_' + type_of_analysis + '.png', dpi=360)
    fig.clf()
    plt = sns.violinplot(np.log10(col_sums + 1))
    fig = plt.get_figure()
    fig.savefig(os.path.splitext(input_file)[0] + '_log10_col_' + type_of_analysis + '.png', dpi=360)
    if filter_data or norm_col:
        filter_and_normalize(cell_ranger, col_sum_table, col_sums, filter_data, hdf5, id_list, ids, in_mat_num,
                             input_file, mult_by, norm_col, remove_zero)


def filter_and_normalize(cell_ranger, col_sum_table, col_sums, filter_data, hdf5, id_list, ids, in_mat_num,
                         input_file, mult_by, norm_col, remove_zero):

    dset = None
    if filter_data:
        # parse the filter rule
        try:
            float(eval(filter_data))
        except ValueError:
            lower_bound, upper_bound = filter_data.split(',')
            lower_bound = float(eval(lower_bound))
            upper_bound = float(eval(upper_bound))
        else:
            lower_bound = float(eval(filter_data))
            upper_bound = None
        print('upper bound set to:', upper_bound)
        print('lower bound set to:', lower_bound)
        # which cells pass the lower bound filter
        lower_bound_bool = np.array(col_sums >= lower_bound, dtype=bool)
        if upper_bound:
            upper_bound_bool = np.array(col_sums <= upper_bound, dtype=bool)
        else:
            upper_bound_bool = np.array([True] * np.shape(col_sums)[0], dtype=bool)
        final_pass = np.array(lower_bound_bool * upper_bound_bool, dtype=bool)
        print(np.sum(final_pass), 'passed')
        col_ids = []
        pass_idxs = []
        for i, row in enumerate(col_sum_table):
            col_sum_table[i].append(final_pass[i])
            if final_pass[i]:
                col_ids.append(row[0])
                pass_idxs.append(i)

        if cell_ranger or hdf5:
            if remove_zero:
                filtered_id_list = []
                keep_row_ids = []
                for i, id_val in enumerate(id_list):
                    keep_row_ids.append(i)
                    filtered_id_list.append(id_val)

            in_mat_num = in_mat_num[:, pass_idxs]
            outfile = os.path.splitext(input_file)[0] + '_filtered.hdf5'
            file_handle = h5py.File(outfile, "w")

            # set up the data matrix (this assumes float32)
            dset = file_handle.create_dataset("infile", (len(id_list), len(col_ids)), dtype=np.float32)

            dset[:, :] = in_mat_num[:, :]

            make_file('\n'.join(id_list), os.path.splitext(input_file)[0] + "_filtered_row_ids.txt")
            make_file('\n'.join(["variables"] + col_ids), os.path.splitext(input_file)[0] +
                      "_filtered_col_ids.txt")
            col_sums = np.array(col_sums)[pass_idxs]
            col_sums = col_sums.tolist()

            file_handle.close()

        else:
            in_mat_num = in_mat_num[:, pass_idxs]
    else:
        pass_idxs = list(range(len(ids) - 1))  # -1 for the title line
    if norm_col:
        print('preparing to normalize columns')
        outfile = os.path.splitext(input_file)[0] + '_norm.hdf5'
        f_norm = h5py.File(outfile, "w")

        # set up the data matrix (this assumes float32)
        dset_2 = f_norm.create_dataset("infile", (len(id_list), len(pass_idxs)), dtype=np.float32)

        # setup this output matrix to start as equal to
        try:  # this one will work if we did filtering
            dset_2[:, :] = dset[:, :]
        except Exception:  # if we didn't, use the original matrix
            dset_2[:, :] = in_mat_num[:, :]

        if np.shape(dset_2[1]) != (len(col_sums),):
            # check that the matrix shape is the same as
            sys.exit("incompatible shapes:" + str(np.shape(dset[1])) + str(len(col_sums)))

        print('multiplying...')
        for i in range(0, np.shape(dset_2)[0]):
            dset_2[i, :] *= mult_by
        print('divinding by sums')
        for i, col in enumerate(col_sums):
            if i % 10 == 0:
                print('\t', i, '\t', 100 * i / len(col_sums))
            dset_2[:, i] /= col
        print(np.sum(dset_2, axis=0))

        f_norm.close()

    # Write the output file


if __name__ == "__main__":
    main()
