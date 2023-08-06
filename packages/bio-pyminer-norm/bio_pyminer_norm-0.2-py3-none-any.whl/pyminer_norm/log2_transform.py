import fileinput
import argparse
import numpy as np
import h5py
import os

from pyminer_norm.common_functions import strip_split


def parse_arguments(parser=None):
    """ Define the arguments available on the command line."""
    if not parser:
        parser = argparse.ArgumentParser()

    parser.add_argument("-input_matrix", '-i',
                        help="the input matrix which needs to be transformed")
    parser.add_argument("-output_matrix", '-o',
                        help="the file which will contain the log2 transformed matrix")
    parser.add_argument("-leading_cols",
                        help="the number of columns on the left which contain non-float descriptive information",
                        default=1,
                        type=int)
    parser.add_argument("-hdf5",
                        help="if the file is a pyminer hdf5 file",
                        action="store_true",
                        default=False)
    parser.add_argument("-concat_leading_cols",
                        help="the input matrix which needs to be transformed",
                        type=bool)
    parser.add_argument("-concat_delim",
                        help="the delimeter which will be used to concatenate the first '-leading cols'",
                        type=str,
                        default='|')
    parser.add_argument("-output_delim",
                        help="the delimeter which will be used to concatenate the the matrix columns",
                        type=str,
                        default='\t')
    args = parser.parse_args()
    return args


def main():
    """ Warpper to run the code in this file from the command line."""
    args = parse_arguments()

    if os.path.isfile(args.output_matrix):
        os.remove(args.output_matrix)

    log2_transform(args.input_matrix, args.output_matrix, args.concat_leading_cols, args.leading_cols,
                   args.concat_delim, args.output_delim, args.hdf5)


def log2_transform(input_matrix, output_matrix, concat_leading_cols=False, leading_cols=1,
                   concat_delim='|', output_delim='\t', hdf5="False"):

    if not hdf5:
        proces_not_hdf5(input_matrix, output_matrix, concat_leading_cols, leading_cols,
                        concat_delim, output_delim)
    else:
        process_hdf5(input_matrix, output_matrix)


def process_hdf5(input_matrix, output_matrix):
    if os.path.isfile(output_matrix):
        os.remove(output_matrix)

    h5f = h5py.File(input_matrix, 'r')
    in_mat_num = h5f["infile"]
    out_mat_file = h5py.File(output_matrix, 'w')
    out_mat_file.create_dataset("infile", np.shape(in_mat_num), dtype=np.float32, maxshape=(None, None))
    out_mat = out_mat_file["infile"]
    for i in range(0, np.shape(in_mat_num)[0]):
        if i%5000==0 and i!=0:
            print("log transforming row:",i)
        out_mat[i, :] = np.log2(in_mat_num[i, :] + 1)
    h5f.close()
    out_mat_file.close()
    print("\n\nfinished!\nThe output file:", output_matrix,"\n is now ready to use\n")
    return()


def proces_not_hdf5(input_matrix, output_matrix, concat_leading_cols, leading_cols, concat_delim, output_delim):
    with open(output_matrix, 'w') as file_handle:
        first = True
        for line in fileinput.input(input_matrix):
            if first:
                # print(line[:500])
                first = False
                temp_line = strip_split(line)
                # print(temp_line[:2])
                # print(len(temp_line))
                if concat_leading_cols:
                    leaders = concat_delim.join(temp_line[:leading_cols])
                else:
                    leaders = temp_line[:leading_cols]

                followers = temp_line[leading_cols:]
                if isinstance(leaders, list):
                    transformed_line = leaders + followers
                else:
                    transformed_line = [leaders] + followers

                # print(transformed_line[3514-15:3514])
                # print(transformed_line[3514-15:])
                transformed_line = output_delim.join(transformed_line)
                transformed_line = transformed_line + '\n'
                file_handle.write(transformed_line)
            else:
                # print(line[:500])
                temp_line = strip_split(line)
                # print(len(temp_line))
                # print(temp_line[:2])
                if concat_leading_cols:
                    leaders = concat_delim.join(temp_line[:leading_cols])
                else:
                    leaders = temp_line[:leading_cols]
                log_transformed = list(np.log2(np.array(temp_line[leading_cols:], dtype=float) + 1))
                if isinstance(leaders, list):
                    transformed_line = leaders + list(map(str, log_transformed))
                else:
                    transformed_line = [leaders] + list(map(str, log_transformed))
                # print(len(transformed_line))
                # print(transformed_line[:15])
                # print(transformed_line[3514:(3514+15)])
                # sys.exit()
                transformed_line = output_delim.join(transformed_line)

                transformed_line = transformed_line + '\n'
                file_handle.write(transformed_line)
                # sys.exit()


if __name__ == "__main__":
    main()
