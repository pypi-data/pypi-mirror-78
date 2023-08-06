import argparse
import fileinput
import os
import numpy as np
import h5py
from pyminer_norm.common_functions import strip_split, read_table, read_file, write_table, make_file


def parse_arguments(parser=None):
    """ Define the arguments available on the command line."""
    if not parser:
        parser = argparse.ArgumentParser()

    parser.add_argument("-input_file", "-i",
                        help="the input matrix which needs to have cols removed")
    parser.add_argument("-output_file", "-o",
                        help="the file which will contain the cleaned matrix")
    parser.add_argument("-remove", "-remove_cols", "-r",
                        help="The file containing the names of columns to remove")
    parser.add_argument("-keep", "-keep_cols", "-k",
                        help="The file containing the names of columns to keep")
    parser.add_argument("-hdf5", "-h5", 
                        action="store_true",
                        help="If we're filtering an hdf5 file")
    parser.add_argument("-ID_list", "-ids", 
                        help="If using the hdf5 file format, feed in the ID_list annotation file. This usually has the gene names in them.")
    parser.add_argument("-columns", "-cols", 
                        help="If using the hdf5 file format, feed in the column annotation file. This usually has the cell names in them.")
    args = parser.parse_args()
    return args


def main():
    """ Warpper to run the code in this file from the command line."""
    args = parse_arguments()

    remove_columns(args.input_file, remove = args.remove, keep = args.keep, output_file = args.output_file, hdf5=args.hdf5, ids=args.ID_list, columns=args.columns)


def remove_columns(input_file, remove = None, keep = None, output_file=None, hdf5=False, ids=None, columns=None, force=False):
    if not force and os.path.isfile(output_file):
        if not hdf5:
            return(read_table(output_file))

    ## get the header
    if not hdf5:
        ## if it's a text file
        header = None
        first = True
        num_lines = 0
        for line in fileinput.input(input_file):
            if first:
                header = strip_split(line)
                first = False
            else:
                pass
            num_lines += 1
        fileinput.close()
    else:
        ## read in the hdf5 file
        h5f_in = h5py.File(input_file, 'r')
        if "infile" in h5f_in:
            in_mat = h5f_in["infile"]
            header = read_file(columns)
            chromium = False
        elif "matrix" in h5f_in:
            chromium = True
            in_mat = h5f_in["matrix"]["data"]
            header = ['variables'] + [res.decode("utf-8") for res in h5f_in['matrix']['barcodes'][:].tolist()]
            ids = [res.decode("utf-8") for res in h5f_in['matrix']['features']['id'][:].tolist()]

    ## read in the filtering parameters
    if keep == None:
        print("\ndoing removal")
        remove = set(read_file(remove, 'lines'))
    else:
        print("\ndoing keep")
        keep = set(read_file(keep, 'lines'))

    ## do the filtering
    remove_indices = []
    keep_indices = []
    for i, line in enumerate(header):
        if remove != None:
            if line in remove:## remove it
                if not hdf5:
                    remove_indices.append(i)
                else:## minus 1 because header included in text file, but not numeric matrix
                    remove_indices.append(i-1)
            else:## we're keeping it
                if not hdf5:
                    keep_indices.append(i)
                else:## minus 1 because header included in text file, but not numeric matrix
                    keep_indices.append(i-1)
        else:
            ## this means that we're doing keep
            #print(line, line not in keep, (i!=0), (line not in keep) and (i!=0))
            #print(keep)
            line_no_q = line.replace('"','')
            if not hdf5:
                if ((line not in keep) and (line_no_q not in keep)) and (i!=0) :
                    remove_indices.append(i)
                else:
                    keep_indices.append(i)
            else:
                if i==0:
                    pass
                else:
                    if ((line not in keep) and (line_no_q not in keep)):
                        ## offset because the text of the column has the leader, but the actual numeric matrix does not
                        ## note that this is the remove_indices list pertaining to the MATRIX, not the header
                        ## the header remove indices would be this vector plus 1
                        remove_indices.append(i-1)
                    else:
                        keep_indices.append(i-1)

    print("\n\n",output_file,"\n\n")
    if output_file:
        print('writing output file')
        # np.savetxt(output_file, in_mat, fmt='%5s', delimiter='\t')
        if not hdf5:
            # make the output file
            
            if os.path.isfile(output_file):
                os.remove(output_file)
            f = open(output_file,'a')
            #for i in range(0,len(in_mat)):
            counter = 0
            for line in fileinput.input(input_file):
                if counter%1000 == 0:
                    print('\t',counter)
                #temp_line = np.array(in_mat[i])
                temp_line = np.array(strip_split(line))
                out_line = list(temp_line[keep_indices])
                out_line = '\t'.join(out_line)
                if counter != num_lines:
                    out_line += '\n'
                f.writelines(out_line)
                counter+=1
            fileinput.close()
            f.close()
            #out_mat = np.delete(in_mat, remove_indices, axis=1)
            #write_table(out_mat, output_file)
            return(read_table(output_file))
        else:
            ## write the hdf5 output
            h5f_out = h5py.File(output_file, 'w')
            keep_indices = [x for x in list(range(len(header)-1)) if x not in {r:None for r in remove_indices} ]
            print("Sanity check:",len(keep_indices) == (len(header)-1) - len(remove_indices))
            out_mat = h5f_out.create_dataset("infile", 
                                             (in_mat.shape[0], len(keep_indices)), 
                                             dtype=np.float32)
            ## make the new columns out file
            new_header = [header[0]]+[header[i+1] for i in keep_indices]
            make_file('\n'.join(new_header),output_file+"_columns.txt")

            # # go through each row & subset the appropriate columns
            for i in range(out_mat.shape[1]):
                if i % 200 == 0:
                    print(i,i/out_mat.shape[1])
                out_mat[:,i] = in_mat[:,keep_indices[i]]
            print(out_mat[:,:] == in_mat[:,keep_indices])
            # out_mat[:,list(range(out_mat.shape[1]))] == in_mat[:,keep_indices]

            ## second sanity check
            print("second sanity check:",out_mat[0,:] == in_mat[0,keep_indices])
            h5f_out.close()
            h5f_in.close()

    else:
        return in_mat


if __name__ == "__main__":
    main()
