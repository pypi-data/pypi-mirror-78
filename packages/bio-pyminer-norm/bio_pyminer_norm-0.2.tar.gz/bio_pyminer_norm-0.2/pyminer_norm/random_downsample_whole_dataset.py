import os
import random
import argparse
from collections import Counter
from matplotlib import use
use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from pyminer_norm.common_functions import read_table, run_cmd


RANDOM_SEED = 123456789


def parse_arguments(parser=None):
    """ Define the arguments available on the command line."""
    if not parser:
        parser = argparse.ArgumentParser()

    parser.add_argument("-infile", '-i',
                        default="/media/scott/HD2/norm_comparison/input/neuron_1k/neuron_1k_v3.tsv",
                        help="the input expression matrix")

    parser.add_argument("-out", '-o',
                        default="/media/scott/HD2/norm_comparison/input/neuron_1k_ds50prcnt/neuron_1k_v3_50pcnt_ds.tsv",
                        help="the input expression matrix")

    parser.add_argument('-fig',
                        help="make the downsampled figure",
                        action="store_true",
                        default=False)

    parser.add_argument("-percent",
                        default=.50,
                        type=float,
                        help="the percent of the dataset to keep from downsampling. Default = 0.50 (i.e.: 50 percent)")

    args = parser.parse_args()
    return args


def make_colsums_equal(expression_vect, num_transcripts):
    return expression_vect * num_transcripts / np.sum(expression_vect) * 10


def get_transcript_vect(index, expression, mult_factor=1):
    return [index] * int(expression * mult_factor)


def get_all_transcript_vect(full_expression_vect, num_genes, num_final_transcripts=int(1e6), sample_percent=0.9):
        # num_final_transcripts = int(1e6)
    full_transcript_vect = []
    # go through each gene, generating a model of the transcriptome for that cell
    for i in range(0, np.shape(full_expression_vect)[0]):
        temp_transcripts = get_transcript_vect(i, full_expression_vect[i])
        full_transcript_vect += temp_transcripts
    # print(np.shape(full_transcript_vect))
    np.random.shuffle(full_transcript_vect)
    full_transcript_vect = np.array(full_transcript_vect)[np.arange(num_final_transcripts, dtype=int)]
    # print(np.shape(full_transcript_vect)[0])
    freq = Counter(full_transcript_vect)
    all_counts = np.zeros(num_genes)
    for i in range(num_genes):
        all_counts[i] = freq[i]
    return all_counts


def rewrite_get_all_transcript_vect(full_data, num_final_transcripts=int(1e6)):

    all_counts = np.zeros(shape=full_data.shape)
    for col_idx, column in enumerate(full_data.T):
        row_set = []
        for gene_idx, UMI_count in enumerate(column):
            for i in range(int(UMI_count)):
                row_set.append(gene_idx)
        random.shuffle(row_set)
        row_set = row_set[:num_final_transcripts]
        for value in row_set:
            all_counts[value][col_idx] += 1
    return all_counts

def new_rewrite_get_transcript_vect(cur_vector, num_final_transcripts=int(1e6)):
    row_set = []
    for gene_idx, UMI_count in enumerate(cur_vector):
            for i in range(int(UMI_count)):
                row_set.append(gene_idx)
    random.shuffle(row_set)
    all_counts = np.zeros((cur_vector.shape))
    for value in row_set:
        all_counts[value] += 1
    return(all_counts)




def downsample_whole_dataset(original_dataset, percent, out, fig=False, force = False):
    if not force and os.path.isfile(out):
        return()

    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    ## check what the type the input was
    if type(original_dataset) == str:
        ## if it was a file, read it in
        if os.path.isfile(original_dataset):
            original_dataset = np.array(read_table(original_dataset))
        else:
            sys.exit("don't know what to do with this input:"+original_dataset)
    elif type(original_dataset) == list:
        ## if it was a list, numpy-fy it
        original_dataset = np.array(original_dataset)

    print("original_dataset:\n",original_dataset,"\n")
    
    full_dataset = np.array(original_dataset[1:, 1:], dtype=float)
    gene_ids = original_dataset[1:, 0]
    cols = original_dataset[0, :]
    num_genes = np.shape(gene_ids)[0]

    # make the output matrix
    print("getting transcript vectors")

    ## create a list that has all counts' row and column entries as 
    all_transcripts = []
    for i in range(full_dataset.shape[0]):
        # if i % 1000 == 0:
        #     print("\t",i)
        non_zero_indices = np.where(full_dataset[i,:] > 0)[0]
        for j in non_zero_indices:
            for count in range(int(full_dataset[i,j])):
                ## this appends a single row, column entry for every count
                all_transcripts.append([i,j])

    out_data = np.zeros((np.shape(full_dataset)[0], np.shape(full_dataset)[1]))
    print("now we're populating the output matrix")
    ## get the random shuffle
    random.shuffle(all_transcripts)
    target_num_transcripts = int(len(all_transcripts)*percent)
    print("\tThe original dataset had",len(all_transcripts),"observed transcripts.")
    print("\tWe'll downsample it to",percent,"percent or:",target_num_transcripts," transcripts.")
    for i in range(target_num_transcripts):
        row = all_transcripts[i][0]
        col = all_transcripts[i][1]
        out_data[row,col]+=1

    if fig:
        print('\nmaking downsampled fig\n')
        plt.clf()
        plt.scatter(np.log2(full_dataset+1), np.log2(out_data+1), s=10)
        plt.savefig(out + ".png")
    # append the gene and column titles
    print('writing the output matrix')

    if os.path.isfile(out):
        os.remove(out)

    with open(out, 'w') as out_f:
        out_f.writelines('\t'.join(cols) + '\n')
        for i, row in enumerate(out_data):
            gene_name = gene_ids[i]
            temp_line = out_data[i, :].tolist()
            temp_line = gene_name + '\t' + '\t'.join(map(str, temp_line))
            if i != len(out_data) - 1:
                out_f.writelines(temp_line + '\n')
            else:
                out_f.writelines(temp_line)

    # out_data = out_data.tolist()
    # for i in range(0,len(out_data)):
    #     out_data[i]=[gene_ids[i]]+out_data[i]
    # out_data = [cols] + out_data
    # #out_data = np.array(out_data)
    # write_table(out_data,args.out)
    print('\ndone!\n')


def main():
    """ Wrapper to run the code in this file from the command line."""
    args = parse_arguments()
    if args.fig:
        print("we'll plot the figure")
    downsample_whole_dataset(args.infile, args.percent, args.out, fig = args.fig)


if __name__ == "__main__":
    main()
