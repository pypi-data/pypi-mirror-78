import argparse
import os
import sys
import fileinput
import numpy as np
import h5py
from pyminer_norm.common_functions import make_file, strip_split, write_table, run_cmd


def parse_arguments(parser=None):
    """ Define the arguments available on the command line."""
    if not parser:
        parser = argparse.ArgumentParser()

    parser.add_argument("-in_dir", "-i",
                        help="the directory which contains the matrices to be combined into a single dataset.")
    parser.add_argument("-in_files",
                        nargs="+",
                        help="the directory which contains the matrices to be combined into a single dataset.")
    parser.add_argument("-output_file", "-o",
                        help="the output file to be made after conversion.")
    parser.add_argument("-hdf5",
                        help="write the output file as an hdf5 file rather than tab delimted.",
                        action='store_true',
                        default=False)
    parser.add_argument("-force",
                        action="store_true",
                        default=False,
                        help = "If force is set to true, we will merge the files even though they differ on the first column. In the case of RNA, this could be from different reference genomes, or something like that. Other times it could be innocuous like two datasets with low expressed genes removed from the datasets, but they were still against the same reference. Proceed with caution!"
                        )
    parser.add_argument("-as_str",
                        action="store_true",
                        default=False,
                        help = "If the matricies you want to combine are str matricies"
                        )
    args = parser.parse_args()
    return args


def get_files_in_folder(in_folder):
    return [f for f in os.listdir(in_folder) if os.path.isfile(os.path.join(in_folder, f))]


def get_sample_names(in_file):
    """ go through all of the files and collect the gene ids and sample_ids"""
    temp_line = None
    for line in fileinput.input(in_file):
        temp_line = strip_split(line)
        break
    fileinput.close()
    temp_line = temp_line[1:]
    top_dir = in_file.split('/')
    file_name = top_dir[-1][:-4]
    for i, field in enumerate(temp_line):
        temp_line[i] = file_name + "||" + field
    return temp_line


def get_genes(in_file):
    gene_list = []
    first = True
    for line in fileinput.input(in_file):
        if first:
            first = False
        else:
            temp_line = strip_split(line)
            gene_list.append(temp_line[0])
    fileinput.close()
    return gene_list


def main():
    """ Warpper to run the code in this file from the command line."""
    args = parse_arguments()

    if args.in_dir is not None:
        os.chdir(args.in_dir)
        all_files = get_files_in_folder(args.in_dir)
    else:
        all_files = args.in_files

    concatenate_matrices_by_col(all_files, args.output_file, args.hdf5, args.force, args.as_str)


def get_unified_row_ids(all_genes):
    all_genes_unified = []
    for gene_list in all_genes:
        all_genes_unified += gene_list
    all_genes_unified = sorted(list(set(all_genes_unified)))
    print("\n there are",len(all_genes_unified), "unique genes\n")
    all_genes_unified_hash = {value:key for key, value in enumerate(all_genes_unified)}
    return(all_genes_unified, all_genes_unified_hash)


def concatenate_matrices_by_col(all_files, output_file, hdf5=False, force = False, as_str = False):
    all_samples = []  # list of lists containing each sample in each dataset
    all_genes = []  # list of lists containing each gene in each dataset
    # this will be a simple linear list with each sample in the order that it will be in the output file
    all_samples_linear = []
    sample_offset = []
    for file in all_files:
        print('working on', file)
        all_samples.append(get_sample_names(file))
        print('\tfound', len(all_samples[-1]), 'new samples')
        print('\t\t', all_samples[-1][:1], "...")
        all_genes.append(get_genes(file))
        print('\tfound', len(all_genes[-1]), 'new genes')
        print('\t\t', all_genes[-1][:1], "...")
    # make all samples linear list
    for sample in all_samples:
        all_samples_linear += sample
    # check that the first column is actually the same in all cases
    for i in range(1, len(all_genes)):
        if all_genes[i - 1] != all_genes[i]:
            print("\n\ngenes are not all the same!")
            # for j in range(len(all_genes[i - 1])):
            #     if all_genes[i - 1][j] != all_genes[i][j]:
            #         print("\n\n\nWARNING\n\n")
            #         print("found discrepancies in the first column in files:\n\t",all_files[i-1],"\n\t",all_files[i])
            #         print("at line#:",j,"\n\t",all_genes[i - 1][j],"\n\t vs \n\t",all_genes[i][j])
            if not force:
                sys.exit('\nexiting because we found discrepancies')
            else:
                print("\n\nTHE FORCE ARGUMENT WAS USED, WE'RE GOING TO MERGE THE FILES ANYWAY!\n\n")
    
    all_row_ids, all_row_ids_hash = get_unified_row_ids(all_genes)
    

    # calculate the column offset for each file
    previous_length = 0
    for sample in all_samples:
        sample_offset.append(previous_length)
        previous_length += len(sample)


    # now we actually start making the output
    h5_f = None
    if hdf5:
        # set up the hdf5 file

        outfile = os.path.splitext(output_file)[0] + '.hdf5'
        if os.path.isfile(outfile):
            os.remove(outfile)
        h5_f = h5py.File(outfile, "w")

        # set up the data matrix (this assumes float32)
        out_mat = h5_f.create_dataset("temp_infile", (len(all_row_ids), len(all_samples_linear)), dtype=np.float32,
                                      maxshape=(None, None),
                                      fillvalue=0.)

        # out_mat = np.zeros((len(all_row_ids),len(all_samples_linear)))

    else:
        if as_str:
            out_mat = np.chararray((len(all_row_ids), len(all_samples_linear)),unicode=True).astype('<U32')
        else:
            out_mat = np.zeros((len(all_row_ids), len(all_samples_linear)))



    # clean the all_samples_linear.. I noticed that quotes sometimes screw things up
    for i, sample_linear in enumerate(all_samples_linear):
        all_samples_linear[i] = sample_linear.replace('"', '')
    
    for file_num, file in enumerate(all_files):
        first = True
        temp_num_samples = 0
        print('\tworking on', file)
        line_count = 0
        for line in fileinput.input(file):
            if first:
                first = False
                temp_num_samples = len(strip_split(line)) - 1
            else:
                line_count+=1
                if temp_num_samples > 2000:
                    if line_count % 2000 == 0:
                        print('\t\t', line_count)
                temp_line = strip_split(line)
                temp_gene = temp_line[0]
                temp_row_idx = all_row_ids_hash[temp_gene]
                if as_str:
                    temp_line_num = np.array(temp_line[1:], dtype='<U32')
                else:
                    temp_line_num = np.array(temp_line[1:], dtype=float)
                # get the gene row(s) to add these values too
                num_samples = np.shape(temp_line_num)[0]
                col_idxs = list(range(sample_offset[file_num], (num_samples + sample_offset[file_num])))
                out_mat[temp_row_idx, min(col_idxs):(max(col_idxs)+1)] = temp_line_num

    print(out_mat)
    print('writing the output file')
    if not hdf5:
        out_str = [["gene"] + all_samples_linear]
        for i, detail in enumerate(out_mat):
            out_str.append([all_row_ids[i]] + detail.tolist())
        out_str = np.array(out_str)

        write_table(out_str, output_file)
    else:
        # create the final dataset with the removed samples and genes
        h5_f.create_dataset("infile", (len(all_row_ids), len(all_samples_linear)),
                            dtype=np.float32, maxshape=(None, None),
                            data=out_mat,
                            fillvalue=0.)

        # double check that it's writing
        out_mat_2 = h5_f["infile"]
        for i in range(0,np.shape(out_mat)[0]):
            out_mat_2[i,:]=out_mat[i,:]

        print("col NonZero Sum", np.sum(h5_f["temp_infile"] != 0.0, axis=0))
        print("colmax", np.max(h5_f["temp_infile"], axis=0))
        print("colmin", np.min(h5_f["temp_infile"], axis=0))
        print('colsum', np.sum(h5_f["temp_infile"], axis=0))
        print(h5_f["temp_infile"])

        print("col NonZero Sum", np.sum(h5_f["infile"] != 0.0, axis=0))
        print("colmax", np.max(h5_f["infile"], axis=0))
        print("colmin", np.min(h5_f["infile"], axis=0))
        print('colsum', np.sum(h5_f["infile"], axis=0))
        print(h5_f["infile"])

        temp = str(output_file).split('/')
        temp = '/'.join(temp[:-1])

        # write the row and column info
        make_file('\n'.join(["variables"] + all_samples_linear), temp + '/column_IDs.txt')
        make_file('\n'.join(all_row_ids), temp + '/ID_list.txt')

        del h5_f["temp_infile"]
        # close the hdf5 file
        h5_f.close()


if __name__ == "__main__":
    main()
