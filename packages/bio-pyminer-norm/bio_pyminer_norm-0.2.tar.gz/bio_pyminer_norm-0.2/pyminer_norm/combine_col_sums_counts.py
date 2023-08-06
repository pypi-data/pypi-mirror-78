# pylint: disable=C0411,C0413
import sys
import os
import argparse
import matplotlib as mpl

mpl.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from pyminer_norm.common_functions import read_table, write_table
from pyminer_norm.col_sums import calculate_col_sum


def parse_arguments(parser=None):
    """ Define the arguments available on the command line."""
    if not parser:
        parser = argparse.ArgumentParser()

    parser.add_argument("--input_files", "--infiles", "-i",
                        nargs="+",
                        help="the input matrices", required=True)

    parser.add_argument("--out", "-o",
                        help="directory for output", required=True)

    args = parser.parse_args()
    return args


def get_pd_df(file_dict, input_files):
    """read in the files"""

    # make empty pd_df
    out_df = {}

    for file in input_files:
        temp_table = np.array(read_table(file_dict[file]))
        temp_vect = np.array(temp_table[1:, 1], dtype=float)
        out_df[file] = temp_vect
    return out_df


def get_individual_scatter(in_file, col_counts_df, col_sums_df, base_dir_dict):
    plt.clf()
    f, ax = plt.subplots(figsize=(6, 6))
    df = pd.DataFrame({"col_counts": col_counts_df[in_file],
                       "col_sums": col_sums_df[in_file]})
    sns.jointplot(x="col_counts", y="col_sums", data=df, kind="kde")
    plt.savefig(base_dir_dict[in_file] + "/col_sums_col_counts.png", dpi=600)
    plt.clf()
    # do it again but on the log scale
    log_counts = np.log10(col_counts_df[in_file] + 1)
    log_sums = np.log10(col_sums_df[in_file] + 1)
    # print(log_counts)
    # print(log_sums)
    df = pd.DataFrame({"log_counts": log_counts,
                       "log_sums": log_sums})
    sns.jointplot(x="log_counts", y="log_sums", data=df, kind="kde")
    plt.savefig(base_dir_dict[in_file] + "/log10_col_sums_col_counts.png", dpi=600)
    plt.clf()


def logify_dict(in_dict):
    all_key = list(in_dict.keys())
    out_dict = {}
    for key in all_key:
        out_dict[key] = np.log10(in_dict[key] + 1)
    return out_dict


def get_combined_scatter(input_files, log_col_counts_df, log_col_sums_df, file_alias_dict, out):
    plt.clf()
    # get the colors
    gradient = np.linspace(0, 1, len(input_files))
    cmap = plt.get_cmap("nipy_spectral")
    # also log it for violin plots
    name_list = []
    log_count_list = []
    log_sum_list = []
    color_vect = []

    for i, in_file in enumerate(input_files):
        temp_color = cmap(i / len(input_files))
        color_vect.append(temp_color)
        print('\t', temp_color)
        log_counts = log_col_counts_df[in_file]
        log_sums = log_col_sums_df[in_file]
        plt.scatter(log_counts, log_sums,
                    c=temp_color, s=0.5, alpha=0.5,
                    label=file_alias_dict[in_file])
        name_list += list([file_alias_dict[in_file]] * len(log_counts))
        log_count_list += log_counts.tolist()
        log_sum_list += log_sums.tolist()
        # log_count_df[name_list[-1]] = log_counts
        # log_sum_df[name_list[-1]] = log_sums
    plt.legend(loc="upper left")
    plt.savefig(out + "/log_counts_vs_log_sums.png", dpi=600)

    # make the dfs
    summary_df = pd.DataFrame({"dataset": name_list, "log_counts": log_count_list, "log_sums": log_sum_list})

    # now plot the violin plots
    plt.clf()
    sns.set(font_scale=0.5)
    sns.violinplot(x="dataset", y="log_counts", data=summary_df)  # ,palette="nipy_spectral")
    plt.savefig(out + "/log_counts_violin.png", dpi=600)
    plt.clf()
    sns.set(font_scale=0.5)
    sns.violinplot(x="dataset", y="log_sums", data=summary_df)  # ,palette="nipy_spectral")
    plt.savefig(out + "/log_sums_violin.png", dpi=600)
    # plt.show()

    out_df = np.array(summary_df, dtype=str).tolist()

    write_table(np.array(summary_df, dtype=str), out + "/combined_statistics.tsv")

    return


def get_col_sums_counts(input_files, out):
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
        base_dir_dict[infile] = os.path.dirname(os.path.abspath(infile))

    # get the dataframe for col_sums
    col_sums_df = get_pd_df(col_sums_file_dict, input_files)
    print(col_sums_df)
    log_col_sums_df = logify_dict(col_sums_df)
    # get the dataframe for col_counts
    col_counts_df = get_pd_df(col_counts_file_dict, input_files)
    print(col_counts_df)
    log_col_counts_df = logify_dict(col_counts_df)
    # get the plots
    for file in input_files:
        get_individual_scatter(file, col_counts_df, col_sums_df, base_dir_dict)

    get_combined_scatter(input_files, log_col_counts_df, log_col_sums_df, file_alias_dict, out)
    return



def main():
    """Run the code in this file from the command line."""
    args = parse_arguments()

    if args.out[-1] != os.sep:
        args.out += os.sep

    ## if the output directory doesn't exist it, make it
    if not os.path.exists(args.out):
        os.makedirs(args.out)

    col_sums_file_dict = {}
    col_counts_file_dict = {}
    file_alias_dict = {}
    base_dir_dict = {}

    print('\n')
    for infile in args.input_files:

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
        base_dir_dict[infile] = os.path.dirname(os.path.abspath(infile))

    # get the dataframe for col_sums
    col_sums_df = get_pd_df(col_sums_file_dict, args.input_files)
    print(col_sums_df)
    log_col_sums_df = logify_dict(col_sums_df)
    # get the dataframe for col_counts
    col_counts_df = get_pd_df(col_counts_file_dict, args.input_files)
    print(col_counts_df)
    log_col_counts_df = logify_dict(col_counts_df)
    # get the plots
    for file in args.input_files:
        get_individual_scatter(file, col_counts_df, col_sums_df, base_dir_dict)

    get_combined_scatter(args.input_files, log_col_counts_df, log_col_sums_df, file_alias_dict, args.out)


if __name__ == "__main__":
    main()
