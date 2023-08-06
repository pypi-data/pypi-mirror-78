import sys
import os
import random
import argparse
import gc
import shutil
import psutil
import tempfile
import h5py
from collections import Counter
from matplotlib import use
import time
use('Agg')
import fileinput
import matplotlib.pyplot as plt
import numpy as np
import ray
import multiprocessing
from scipy.sparse import csc_matrix, csr_matrix, lil_matrix

from pyminer_norm.common_functions import read_table, run_cmd, strip_split, get_indices, ray_dicts_to_array, get_contiguous_indices


def parse_arguments(parser=None):
    """ Define the arguments available on the command line."""
    if not parser:
        parser = argparse.ArgumentParser()

    parser.add_argument("-infile", '-i',
                        default="/media/scott/HD2/imputation/pyminer_dynamic_cutoff/real/PMID_27667667_pancreas"
                                "_refseq_rpkms_3514sc_ge150k_OK_erccRM_ensg_collated_log2_naRM_sigExpress_ENSG.txt",
                        help="the input expression matrix")

    parser.add_argument("-out", '-o',
                        default="/media/scott/HD2/imputation/pyminer_dynamic_cutoff/real/PMID_27667667_pancreas_refse"
                                "q_rpkms_3514sc_ge150k_OK_erccRM_ensg_collated_log2_naRM_sigExpress_ENSG_1e2.txt",
                        help="the input expression matrix")

    parser.add_argument('-log',
                        help="if the input is log2 transformed we'll undo that to make the original "
                             "transcriptome again",
                        action="store_true",
                        default=False)

    parser.add_argument('-fig',
                        help="make the downsampled figure",
                        action="store_true",
                        default=False)

    parser.add_argument("-num_transcripts",
                        default=1e2,
                        type=int,
                        help="the number of transcripts each cell should have")

    parser.add_argument("-processes",
                        default=None,
                        type=int,
                        help="the number of processes to use. Default is the number of cores available on the machine.")

    parser.add_argument("-seed",
                        default=123456789,
                        type=int,
                        help="the random seed")

    parser.add_argument("-force",
                        action = 'store_true',
                        help="if the output already exists, should we overwrite it, or just exit? default: False (i.e.: not forcing)")

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
    row_set = row_set[:num_final_transcripts]
    all_counts = np.zeros((cur_vector.shape))
    for value in row_set:
        all_counts[value] += 1
    return(all_counts)


def cur_vector_to_row_set(cur_vector,num_final_transcripts):
    num_orig_trans = int(np.sum(cur_vector))
    row_set = np.zeros((num_orig_trans),dtype=int)-1000000
    counter=0
    for gene_idx, UMI_count in enumerate(cur_vector):
        #print(gene_idx, UMI_count)
        for i in range(int(UMI_count)):
            row_set[counter]=gene_idx
            counter+=1
    # print(cur_vector)
    # print(cur_vector>0)
    # print(num_orig_trans, counter,num_orig_trans - counter,np.sum(cur_vector>0),np.sum(cur_vector>1))
    # print(row_set)
    return(row_set)


@ray.remote
def ray_new_rewrite_get_transcript_vect_out_of_mem(index_list, 
                                                   process_writing_bool,
                                                   job_num,
                                                   full_input_array=None, 
                                                   full_input_hdf5=None, 
                                                   num_final_transcripts=int(1e6),
                                                   sparse=False, 
                                                   out_data=None, 
                                                   temp_dir=None, 
                                                   max_mem_percent=85):
    gc.enable()
    if full_input_array is None and full_input_hdf5 is not None:
        in_h5 = h5py.File(out_h5_file,'r')
        full_input_array = in_h5["infile"]
    ## set up the temp out file
    min_idx=str(min(index_list))
    max_idx=str(max(index_list))
    temp_out_file = os.path.join(temp_dir, "temp_"+min_idx+'_'+max_idx+".hdf5")
    print("starting temp_file:",temp_out_file)
    out_h5 = h5py.File(temp_out_file,'w')
    ## make the dataset
    num_genes = full_input_array.shape[0]
    out_dims = (num_genes,int(max(index_list)-min(index_list)+1))
    temp_sparse = lil_matrix(out_dims,dtype=np.int32)
    temp_done_vect = np.zeros((out_dims[1]),dtype=bool)
    out_data = out_h5.create_dataset("infile",
                                out_dims,
                                dtype=np.int32)
    #                             fillvalue=0,
    #                             compression='gzip',
    #                             compression_opts=9)
    index_list_dict = {key:value for value, key in enumerate(index_list)}
    temp_col_idx_dict={}
    for col_idx in range(len(index_list)):
        if col_idx%250==0 and col_idx!=0 and job_num==0:
            print(round(col_idx/len(index_list)*100,2),"% ","done")
        cur_idx = index_list[col_idx]
        #start=time.time()
        if type(full_input_array)==np.ndarray:
            cur_vector = full_input_array[:, cur_idx].astype(int)## full input array is in shared memory
        elif type(full_input_array)==csc_matrix:
            cur_vector = np.zeros((num_genes,),dtype=int)
            #start_cast = time.time()
            intermediate = full_input_array[:, cur_idx]
            for i in range(len(intermediate.indices)):
                cur_vector[intermediate.indices[i]] = intermediate.data[i]
            #cast_time = time.time()-start_cast
            #print("cast",cast_time)
        row_set = cur_vector_to_row_set(cur_vector, num_final_transcripts)
        if num_final_transcripts<row_set.shape[0]:
            np.random.shuffle(row_set)
            row_set = row_set[:num_final_transcripts]
        else:
            print("WARNING: cell#",cur_idx,"has fewer or equal transcripts than we're downsampling to:",row_set.shape[0])
        #print('making lil')
        #all_counts = lil_matrix((cur_vector.shape[0],1),dtype=np.int32)
        for value in row_set:
            #all_counts[value,0] += 1
            #out_data[value,col_idx]+=1
            temp_sparse[value,col_idx]+=1
        temp_done_vect[col_idx]=True
        #temp_col_idx_dict[col_idx] = all_counts
        ######### check for percent memory used
        if (psutil.virtual_memory()[2] >= max_mem_percent) or (np.sum(temp_done_vect)>10000 and np.sum(process_writing_bool)==0):
            process_writing_bool[job_num]=True
            print("dumping from memory to file so we don't go over into virtial memory")
            ## get the pertinent indices
            pert_indicies = np.where(temp_done_vect==True)[0]
            min_idx = np.min(pert_indicies)
            max_idx = np.max(pert_indicies)
            print("setting indices:",min_idx,"-", max_idx)
            #for temp_idx in pert_indices:
            #    out_data[:,temp_idx]+=temp_col_idx_dict[col_idx].todense().astype(np.int32).tolist()[0]
            out_data[:,min_idx:(max_idx+1)]+=temp_sparse.tocsc()[:,min_idx:(max_idx+1)]
            del temp_sparse
            gc.collect()
            process_writing_bool[job_num]=False
            temp_sparse = lil_matrix(out_dims,dtype=np.int32)
            temp_done_vect = np.zeros((out_dims[1]),dtype=bool)
            #temp_col_idx_dict = {}
        #all_time = time.time()-start
        #print("time:",all_time,"sec")
        #print('cast percent:',cast_time/all_time)
        #poop
    process_writing_bool
    final_commit_finished = False
    while (not final_commit_finished):
        ## while we haven't finished writing the last results to file yet,
        ## we'll have to wait until the hard drive is free to write the results to file
        ## NOTE: I implemented this waiting step, because it actually takes longer overall
        ## if several jobs are trying to write at the same time. This is because the hard drive 
        ## is spinning around to different locations writing different chunks of data instead of
        ## much more quickly just writing a single large chunk, then moving to the next location on 
        ## the hd for the next job.
        if (np.sum(process_writing_bool)==0):
            process_writing_bool[job_num]=True
            print("writing results for job #",job_num)
            pert_indicies = np.where(temp_done_vect==True)[0]
            if len(pert_indicies)>0:
                #print(pert_indicies)
                min_idx = np.min(pert_indicies)
                max_idx = np.max(pert_indicies)
                print("setting final indices:",min_idx,"-", max_idx)
                #for temp_idx in pert_indices:
                #    out_data[:,temp_idx]+=temp_col_idx_dict[col_idx].todense().astype(np.int32).tolist()[0]
                out_data[:,min_idx:(max_idx+1)]+=temp_sparse.tocsc()[:,min_idx:(max_idx+1)]
            del temp_sparse
            gc.collect()
            final_commit_finished=True
            process_writing_bool[job_num]=False
        else:
            ## take a break before checking again just so the loop isn't needlessly stealing cycles
            time.sleep(5)
    print("\nJob #",job_num,"complete\n")
    # for temp_idx in temp_col_idx_dict.keys():
    #     out_data[:,temp_idx]+=temp_col_idx_dict[col_idx].todense().astype(np.int32).tolist()[0]
    # del temp_col_idx_dict[col_idx]
    ## close the files
    if full_input_hdf5 is not None:
        in_h5.close()
    out_h5.close()
    return(temp_out_file)



@ray.remote
def ray_new_rewrite_get_transcript_vect(full_input_array, index_list, num_final_transcripts=int(1e6),sparse=False, out_data=None):
    ## free_temp_space = shutil.disk_usage(tempfile.gettempdir())[2]
    out_dict = {}
    num_genes = full_input_array.shape[0]
    for cur_idx in index_list:
        #start=time.time()
        if type(full_input_array)==np.ndarray:
            cur_vector = full_input_array[:, cur_idx].astype(int)## full input array is in shared memory
        elif type(full_input_array)==csc_matrix:
            cur_vector = np.zeros((num_genes,),dtype=int)
            #start_cast = time.time()
            intermediate = full_input_array[:, cur_idx]
            for i in range(len(intermediate.indices)):
                cur_vector[intermediate.indices[i]] = intermediate.data[i]
            #cast_time = time.time()-start_cast
            #print("cast",cast_time)
        old_way=False
        if old_way:
            row_set = []
            for gene_idx, UMI_count in enumerate(cur_vector):
                for i in range(int(UMI_count)):
                    row_set.append(gene_idx)
            random.shuffle(row_set)
            #print(num_final_transcripts, len(row_set))
            row_set = row_set[:num_final_transcripts]
        else:
            row_set = cur_vector_to_row_set(cur_vector, num_final_transcripts)
            if num_final_transcripts<row_set.shape[0]:
                np.random.shuffle(row_set)
                row_set = row_set[:num_final_transcripts]
            else:
                print("WARNING: cell#",cur_idx,"has fewer or equal transcripts than we're downsampling to:",row_set.shape[0])
            #############################################
            #print(row_set)
        #print("\t",len(row_set))
        if not sparse:
            all_counts = np.zeros((cur_vector.shape))
            for value in row_set:
                all_counts[value] += 1
        else:
            all_counts = lil_matrix((cur_vector.shape[0],),dtype=np.int32)
            for value in row_set:
                all_counts[value] += 1
        if out_data is not None:
            out_data[:,cur_idx]=all_counts
        else:
            out_dict[cur_idx]=all_counts
        #all_time = time.time()-start
        #print("time:",all_time,"sec")
        #print('cast percent:',cast_time/all_time)
        #poop
    return(out_dict)


def process_input_file(in_file):
    ## first go through & get the columns and gene ids
    print("gathering gene IDs and column names")
    first = True
    gene_ids = []
    for line in fileinput.input(in_file):
        if first:
            first = False
            cols = strip_split(line)
        else:
            temp_line = strip_split(line)
            gene_ids.append(temp_line[0])
    fileinput.close()
    ## now make the output array
    print("creating the input array")
    full_dataset = np.zeros((len(gene_ids), len(cols)-1))
    first = True
    idx = 0
    for line in fileinput.input(in_file):
        if idx % 5000 == 0:
            print("\t",idx)
        if first:
            first = False
        else:
            temp_line = strip_split(line)
            full_dataset[idx,:] = list(map(float,temp_line[1:]))
            idx+=1
    fileinput.close()
    return(np.array(gene_ids), np.array(cols), full_dataset)
    

def process_input(original_dataset):
    ## check what the type the input was
    if type(original_dataset) == str:
        ## if it was a file, read it in
        if os.path.isfile(original_dataset):
            gene_ids, cols, full_dataset = process_input_file(original_dataset)
        else:
            sys.exit("don't know what to do with this input:"+original_dataset)
    elif type(original_dataset) == list:
        ## if it was a list, numpy-fy it
        original_dataset = np.array(original_dataset)
        print("original_dataset:\n",original_dataset,"\n")
        gene_ids = original_dataset[1:, 0]
        cols = original_dataset[0, :]
        full_dataset = np.array(original_dataset[1:, 1:], dtype=float)
    return(gene_ids, cols, full_dataset)


def get_temp_dir(temp_dir):
    if temp_dir == None:
        temp_dir = tempfile.gettempdir()
    if not os.path.isdir(str(temp_dir)):
        if not os.path.isdir(temp_dir):
            print("Couldn't find the supplied temp_dir, using the system temp_dir instead")
        temp_dir = tempfile.gettempdir()
    free_temp_space = shutil.disk_usage(temp_dir)[2]
    print("found",free_temp_space/1000000000,"free Gb in",temp_dir)
    return(temp_dir, free_temp_space)


def collate_ray_h5s(in_h5s, indices, out_h5_file, out_dims):
    ## make the outfile
    out_h5 = h5py.File(out_h5_file,'w')
    ## make the dataset
    out_mat = out_h5.create_dataset("infile",
                                out_dims,
                                dtype=np.int32,
                                fillvalue=0)#,
                                # compression='gzip',
                                # compression_opts=9)
    ## go through the infiles setting the outfile values
    for i in range(len(in_h5s)):
        print("\tcollating:",in_h5s[i])
        temp_h5 = h5py.File(in_h5s[i],'r')
        temp_idxs = indices[i]
        out_mat[:,min(temp_idxs):max(temp_idxs)+1]=temp_h5["infile"][:,:]## +1 because slicing is not inclusive
        temp_h5.close()
    ## close the outfile
    out_h5.close()
    return(out_h5_file)


def downsample_out_of_memory(full_dataset, 
                             gene_ids,
                             cols,
                             num_transcripts,
                             out_h5_file,
                             processes = None,
                             process_mem=20,
                             random_seed=123456789,
                             temp_dir = None):
    """
    Takes in either a sparse matrix, or the path to an hdf5 and downsample in parallel, using temp files in compressed hdf5 format to complete the processes
    """
    start = time.time()
    random.seed(int(random_seed))
    np.random.seed(int(random_seed))
    num_transcripts = int(num_transcripts)
    gene_ids = np.array(gene_ids)
    num_genes = np.shape(gene_ids)[0]
    if processes is None:
        processes = multiprocessing.cpu_count()
    ## look at input file to determine if we can share it, if it's a sparse matrix or if not, and it's an hdf5 file
    if 'shape' in dir(full_dataset):
        is_sparse_mat = True
        is_h5 = False
    elif type(full_dataset)==str:
        if os.path.isfile(full_dataset):
            ## check that it's hdf5
            try:
                h5f = h5py.File(in_file , 'r')
            except:
                sys.exit("can't handle this file, not hdf5")
            else:
                h5f.close()
                is_h5 = True
                is_sparse_mat = False
    ##########################################
    ## get temp_dir info and check it's enough
    temp_dir, free_temp_space = get_temp_dir(temp_dir)
    ##
    if is_sparse_mat:
        if free_temp_space < 2*sys.getsizeof(full_dataset):
            print("The temp_dir ("+temp_dir+") doesn't have enough space unfortunately, please find a new location with enough space on it: ~"+str(2*os.getsizeof(full_dataset)/1000000000)+"Gb likely needed")
            return
    elif is_h5:
        in_file_size = os.path.getsize(full_dataset)
        #needed_bytes = in_file_size * processes + in_file_size * 2
        ## if we can read the same file in paralle, the below will work, but if not, use the above
        needed_bytes = in_file_size * processes + in_file_size * 2
        if free_temp_space < needed_bytes:
            print("The temp_dir ("+temp_dir+") doesn't have enough space unfortunately, please find a new location with enough space on it: ~"+str(needed_bytes/1000000000)+"Gb likely needed")
            return
    ##########################################
    ## start the ray stuff
    index_lists = get_contiguous_indices(processes,full_dataset.shape[1])
    ray_calls = []
    ray.init(memory=int(process_mem*1000000000),object_store_memory=int(process_mem*1000000000))
    process_writing_bool = ray.put(np.zeros((processes,),dtype=bool))
    if is_sparse_mat:
        ## this means that it should be a sparse matrix that we can put in shared memory
        ray_full_dataset = ray.put(full_dataset)
    for p in range(processes):
        ## full_input_array=None, full_input_hdf5=None, num_final_transcripts=int(1e6),sparse=False, out_data=None, temp_dir=None
        if is_sparse_mat:
            ray_calls.append(ray_new_rewrite_get_transcript_vect_out_of_mem.remote(index_lists[p],
                                                                                   process_writing_bool,
                                                                                   p,
                                                                                   full_input_array=ray_full_dataset,
                                                                                   num_final_transcripts=num_transcripts,
                                                                                   temp_dir = temp_dir))
        else:
            ray_calls.append(ray_new_rewrite_get_transcript_vect_out_of_mem.remote(index_lists[p],
                                                                                   process_writing_bool,
                                                                                   p,
                                                                                   full_input_hdf5=full_dataset,
                                                                                   num_final_transcripts=num_transcripts,
                                                                                   temp_dir = temp_dir))
    ray_responses = ray.get(ray_calls)
    ray.shutdown()
    ## ray responses are the names of the hdf5 files that the results were written to.
    print("finished individual jobs. Now we'll collate them into a single hdf5 file. (This could take a few min)")
    collate_ray_h5s(ray_responses, index_lists, out_h5_file, full_dataset.shape)
    print("finished downsampling in:",round((time.time()-start)/60,2),'min')
    print("cleaning up temp files")
    for temp_file in ray_responses:
        rm(temp_file)
    print("\n\n\ndone!")
    return(out_h5_file)


def downsample(original_dataset, 
               num_transcripts, 
               out, 
               plot=False, 
               log=False, 
               force = False, 
               processes = None, 
               random_seed=123456789,
               process_mem=20,
               gene_ids=None,
               cols=None,
               full_dataset=None,
               sparse=False,
               out_h5=False,
               out_h5_sparse=False):
    if out is not None:
        if not force and os.path.isfile(out):
            return()
    random.seed(random_seed)
    np.random.seed(random_seed)
    num_transcripts = int(num_transcripts)
    ## read in the file
    if type(original_dataset)==str:
        if os.path.isfile(original_dataset):
            ## if the input was a tsv file
            print("reading in tsv")
            gene_ids, cols, full_dataset = process_input(original_dataset)
    elif (gene_ids is not None) and (cols is not None) and (full_dataset is not None):
        print("called programmatically with matrix, genes, and cols")
        gene_ids = np.array(gene_ids)
    ## 
    num_genes = np.shape(gene_ids)[0]
    # undo the log if we need to
    if log:
        print(np.sum(full_dataset, axis=0))
        full_dataset[:, :] = 2 ** full_dataset[:, :]
        full_dataset[:, :] -= 1
        print(np.sum(full_dataset, axis=0))
        print(np.shape(np.sum(full_dataset, axis=0)))
    # make the output matrix
    print("getting transcript vectors")
    ##### <this section before ray> #######
    start = time.time()
    if processes == 1:
        if not sparse:
            out_data = np.zeros((np.shape(full_dataset)[0], np.shape(full_dataset)[1]))
        else:
            out_data = csc_matrix((np.shape(full_dataset)[0], np.shape(full_dataset)[1]))
        # out_data = rewrite_get_all_transcript_vect(full_data=full_dataset, num_final_transcripts=num_transcripts)
        for i in range(0, np.shape(full_dataset)[1]):
            if i % 250 == 0:
                print('\t', i)
            out_data[:, i] = new_rewrite_get_transcript_vect(full_dataset[:, i],num_final_transcripts = num_transcripts)
        ##### </this section before ray> #######
        #########################################
    else:
        ######### <ray parallelized> ############
        if processes == None:
            processes = multiprocessing.cpu_count()
        ray_calls = []
        ray.init(memory=int(process_mem*1000000000),object_store_memory=int(process_mem*1000000000))
        if sparse:
            ray_out_data = ray.put(csc_matrix((np.shape(full_dataset)[0], np.shape(full_dataset)[1]),dtype=np.int32))
        ray_full_dataset = ray.put(full_dataset)
        index_lists = get_indices(processes,full_dataset.shape[1])
        for p in range(processes):
            if sparse:
                ray_calls.append(ray_new_rewrite_get_transcript_vect.remote(ray_full_dataset, index_lists[p], num_final_transcripts = num_transcripts, sparse=sparse, out_data = ray_out_data))
            else:
                ray_calls.append(ray_new_rewrite_get_transcript_vect.remote(ray_full_dataset, index_lists[p], num_final_transcripts = num_transcripts, sparse=sparse))
        out_dicts = ray.get(ray_calls)
        if sparse:
            out_data = ray.get(ray_out_data)
        ray.shutdown()
        if not sparse:
            out_data = ray_dicts_to_array(out_dicts, dicts_are_cols=True)
        del out_dicts
    print("took:",time.time()-start,"seconds")
    print("in_shape:",full_dataset.shape)
    print("out_shape:",out_data.shape)
    ######### </ray parallelized> ############
    ##########################################
    # re-log transform it if we need to do that
    if log:
        # print(np.sum(np.log2(out_data+1),axis=0))
        out_data = np.log2(out_data + 1)
        if plot:
            full_dataset = np.log2(full_dataset + 1)
    if plot:
        print('\nmaking downsampled fig\n')
        plt.clf()
        plt.scatter(np.log2(full_dataset+1), np.log2(out_data+1), s=5)
        plt.xlabel("input data")
        plt.ylabel("output data")
        plt.savefig(out + ".png")
    #####################################
    ## if there is no out file given, we'll just return the matrix
    if out==None:
        return(out_data)
    ## otherwise, write the output matrix
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
    print('\ndone downsampling and writing output!\n')
    return()
#######################################


def main():
    """ Wrapper to run the code in this file from the command line."""
    args = parse_arguments()

    downsample(args.infile, 
               args.num_transcripts, 
               args.out, 
               args.fig, 
               args.log, 
               force = args.force, 
               random_seed = args.seed,
               processes = args.processes)

if __name__ == "__main__":
    main()
