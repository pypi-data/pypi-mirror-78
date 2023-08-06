import sys
import os
import argparse

import numpy as np
from pyminer_norm.common_functions import read_table, make_file
from pyminer_norm.remove_columns import remove_columns
from pyminer_norm.downsample import downsample
from pyminer_norm.log2_transform import log2_transform
from pyminer_norm.concatenate_matricies_by_col import concatenate_matrices_by_col
from pyminer_norm.col_sums import calculate_col_sum

def parse_arguments(parser=None):
    """ Define the arguments available on the command line."""
    if not parser:
        parser = argparse.ArgumentParser()

    parser.add_argument("--input_files", "--i", "--infiles","-input_files", "-i", "-infiles",
                        nargs="+",
                        help="the input matrices in tsv format", required=True)
    
    parser.add_argument("--sum_range", "--s_range", "--sr","-sum_range", "-s_range", "-sr",
                        help="the lower and upper bounds of what should be included in "
                             "the final dataset for the sums (ie. '4000,inf')", default='4000,inf')
    
    parser.add_argument("--count_range", "--c_range", "--cr","-count_range", "-c_range", "-cr",
                        help="the lower and upper bounds of what should be included in "
                             "the final dataset for the counts (i.e.: '2500,4000')", default='2500,4000')
    
    parser.add_argument("--downsample", "--ds","-downsample","-ds",
                        type=int,
                        help="by default, this will downsample to 100%% of the minimum total "
                             "UMI in the cell that is kept with the least UMI. For example "
                             "the lower cutoff you give for sum_range is 3162, "
                             "then the default downsample value will be 3003 (i.e.: 100%% of 3162)",
                        )
    
    parser.add_argument("-force_concat",
                        help="If the reference genomes were the same, but in a different order, or non-expressed genes removed, use this to concatenate the matrices anyway.",
                        action = 'store_true')

    parser.add_argument("--out", "--final_output", "-o","-out",
                        help="the PREFIX for the final output file (without extension). Note that this is not a directory or a full file name - this  will be the beginning of the name for a couple files that will be generated.", required=True)



    args = parser.parse_args()
    return args


def get_removal_list(table, temp_min, temp_max):
    """go through the files and get the samples we want to remove"""
    temp_removal_list = []
    # read in the sums file
    temp_col_sums = read_table(table)
    for i in range(1, len(temp_col_sums)):
        temp_sum = temp_col_sums[i][1]
        if temp_sum < temp_min or temp_sum > temp_max:
            temp_removal_list.append(temp_col_sums[i][0])
    return temp_removal_list


def get_min_max(in_str):
    """process arguments for min and max of counts and sums"""
    s_range = in_str.split(',')
    s_vect = []
    for value in s_range:
        if value == '-inf':
            s_vect.append(np.NINF)
        elif value == 'inf':
            s_vect.append(np.inf)
        else:
            try:
                s_vect.append(eval(value))
            except ValueError:
                raise Exception("could not convert " + value + " to numeric")
    # s_vect = [x for eval(x) in in_str]
    s_min = min(s_vect)
    s_max = max(s_vect)
    return s_min, s_max


def main():
    """ Warpper to run the code in this file from the command line."""
    args = parse_arguments()

    # script_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

    process(input_files=args.input_files,
            sum_range=args.sum_range,
            count_range=args.count_range,
            out=args.out,
            downsample_val=args.downsample,
            force_concat = args.force_concat)


def process(input_files, sum_range, count_range, out, downsample_val=0, force_concat = False):
    col_sums_file_dict = {}
    col_counts_file_dict = {}
    file_alias_dict = {}
    base_dir_dict = {}
    print('\n')
    for infile in input_files:

        if os.path.isfile(infile):
            print("found", infile)
            file_alias_dict[infile] = os.path.basename(infile)
        else:
            sys.exit("couldn't find " + infile + "!")
        # first check if col_sums has been called
        temp_colsums_file = infile[:-4] + "_col_sum.txt"
        if not os.path.isfile(temp_colsums_file):
            calculate_col_sum(infile)

        # first check if col_count has been called
        temp_colcount_file = infile[:-4] + "_col_count.txt"
        if not os.path.isfile(temp_colcount_file):
            calculate_col_sum(infile, type_of_analysis="count")

        col_sums_file_dict[infile] = temp_colsums_file
        col_counts_file_dict[infile] = temp_colcount_file
        base_dir_dict[infile] = os.path.dirname(os.path.abspath(infile)) + "/"
    s_min, s_max = get_min_max(sum_range)
    c_min, c_max = get_min_max(count_range)
    if not downsample_val:
        ## if downsample is not actually give, set it to the default which is just the minimum to include threshold
        downsample_val = int(s_min)
    # make the string to append to the output file
    sum_count_add_str = "_Sum" + str(s_min) + "to" + str(s_max) + "_Count" + str(c_min) + "to" + str(c_max) + ".tsv"
    # log the final output files so that we can combine them
    final_processed_list = []
    for infile in input_files:
        print("processing:", file_alias_dict[infile])
        temp_rm_list = get_removal_list(col_sums_file_dict[infile], s_min, s_max)
        temp_rm_list += get_removal_list(col_counts_file_dict[infile], c_min, c_max)
        temp_rm_list = list(set(temp_rm_list))
        print("\tremoving", len(temp_rm_list))

        # write the removal list
        print("writing the removal list...")
        rm_file_name = base_dir_dict[infile] + "rm_samples.txt"
        make_file('\n'.join(temp_rm_list), rm_file_name)

        # remove_them
        print("Removing columns...")
        temp_outfile = infile[:-4] + sum_count_add_str
        remove_columns(infile, remove = rm_file_name, output_file = temp_outfile)

        # now downsample it
        print("downsampling...")
        temp_outfile_ds = temp_outfile[:-4] + "_ds" + str(downsample_val) + ".tsv"
        downsample(temp_outfile, downsample_val, temp_outfile_ds)

        final_processed_list.append(temp_outfile_ds)
    # merge the files and log transform
    print("merge the files and log transform")

    concatenate_matrices_by_col(final_processed_list, out + ".hdf5", hdf5=True, force = force_concat)
    log2_transform(out + ".hdf5", out + "_log2.hdf5", hdf5=True)


if __name__ == "__main__":
    main()
