import fileinput
import os
import argparse
from pyminer_norm.common_functions import process_dir, get_indices, strip_split



def get_target_file_names(main_path, num_files, in_file):
    in_file_name = os.path.basename(in_file)
    in_file_name = os.path.splitext(in_file_name)[0]
    dir_for_splits = process_dir(os.path.join(main_path,"processing"))
    file_names = []
    for i in range(num_files):
        file_names.append(os.path.join(dir_for_splits,in_file_name+"_"+str(i)+".tsv"))
    return(file_names)


def get_target_cols(top_line, num_files):
    ## a list of lists
    chunk_size = int((len(top_line)-1) / num_files)
    start_idxs = [1]
    end_idxs = [chunk_size+1]
    sample_list = []
    for i in range(num_files-1):
        start_idxs.append(start_idxs[-1]+chunk_size)
        end_idxs.append(end_idxs[-1]+chunk_size)
    end_idxs[-1]=len(top_line)
    return(start_idxs, end_idxs)


def open_files(all_target_files):
    out_files = []
    for target in all_target_files:
        out_files.append(open(target, 'w'))
    return(out_files)


def update_files(out_files, temp_line, start_idxs, end_idxs):
    for i in range(len(out_files)):
        out_line = '\t'.join([temp_line[0]]+temp_line[start_idxs[i]:end_idxs[i]])+'\n'
        out_files[i].write(out_line)
    return(out_files)


def do_splits(in_file, all_target_files, start_idxs, end_idxs):
    out_files = open_files(all_target_files)
    for line in fileinput.input(in_file):
        temp_line = strip_split(line)
        out_files = update_files(out_files, temp_line, start_idxs, end_idxs)
    for file in out_files:
        file.close()
    return()


def make_split_files(in_file, cutoff, samples):
    main_path = os.path.dirname(in_file)
    num_files = int(len(samples)/cutoff)+1
    all_target_files = get_target_file_names(main_path, num_files, in_file)
    start_idxs, end_idxs = get_target_cols(samples, len(all_target_files))
    do_splits(in_file, all_target_files, start_idxs, end_idxs)
    return(all_target_files)


def file_needs_splitting(in_file, cutoff):
    for line in fileinput.input(in_file):
        top_line = strip_split(line)
        break
    fileinput.close()
    return(len(top_line) > cutoff, top_line)


def get_split_dict_list(in_file, cutoff):
    needs_split, top_line = file_needs_splitting(in_file, cutoff)
    if needs_split:
        in_files = make_split_files(in_file, cutoff, top_line)
        return(in_file)
    else:
        return([in_file])


def split_all_files_if_needed(in_files, cutoff):
    split_dict = {}
    for temp_file in in_files:
        split_dict[temp_file] = get_split_dict_list(temp_file, cutoff)
    return(split_dict)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-input_files", "-i",
                        nargs="+",
                        help="the input matrices",
                        required=True)
    parser.add_argument("-cutoff", "-c",
                        help="the cutoff for the maximum number of columns in a matrix to not split it.",
                        default = 15000,
                        type=int,
                        required=False)
    args = parser.parse_args()
    split_all_files_if_needed(args.input_files, args.cutoff)