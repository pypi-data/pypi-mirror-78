
##import dependency libraries
import sys,time,glob,os,pickle,fileinput,argparse
from heapq import nlargest
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
import pandas as pd
import random
##############################################################
## basic function library
def read_file(tempFile,linesOraw='lines',quiet=False):
    if not quiet:
        print('reading',tempFile)
    f=open(tempFile,'r')
    if linesOraw=='lines':
        lines=f.readlines()
        for i in range(0,len(lines)):
            lines[i]=lines[i].strip('\n')
    elif linesOraw=='raw':
        lines=f.read()
    f.close()
    return(lines)

def make_file(contents,path):
    f=open(path,'w')
    if isinstance(contents,list):
        f.writelines(contents)
    elif isinstance(contents,str):
        f.write(contents)
    f.close()

    
def flatten_2D_table(table,delim):
    #print(type(table))
    if str(type(table))=="<class 'numpy.ndarray'>":
        out=[]
        for i in range(0,len(table)):
            out.append([])
            for j in range(0,len(table[i])):
                try:
                    str(table[i][j])
                except:
                    print(table[i][j])
                else:
                    out[i].append(str(table[i][j]))
            out[i]=delim.join(out[i])+'\n'
        return(out)
    else:
        for i in range(0,len(table)):
            for j in range(0,len(table[i])):
                try:
                    str(table[i][j])
                except:
                    print(table[i][j])
                else:
                    table[i][j]=str(table[i][j])
            table[i]=delim.join(table[i])+'\n'
    #print(table[0])
        return(table)

def strip_split(line, delim = '\t'):
    return(line.strip('\n').split(delim))

def make_table(lines,delim):
    for i in range(0,len(lines)):
        lines[i]=lines[i].strip()
        lines[i]=lines[i].split(delim)
        for j in range(0,len(lines[i])):
            try:
                float(lines[i][j])
            except:
                lines[i][j]=lines[i][j].replace('"','')
            else:
                lines[i][j]=float(lines[i][j])
    return(lines)


def get_file_path(in_path):
    in_path = in_path.split('/')
    in_path = in_path[:-1]
    in_path = '/'.join(in_path)
    return(in_path+'/')


def read_table(file, sep='\t'):
    return(make_table(read_file(file,'lines'),sep))
    
def write_table(table, out_file, sep = '\t'):
    make_file(flatten_2D_table(table,sep), out_file)
    

def import_dict(f):
    f=open(f,'rb')
    d=pickle.load(f)
    f.close()
    return(d)

def save_dict(d,path):
    f=open(path,'wb')
    pickle.dump(d,f)
    f.close()

def cmd(in_message, com=True):
    print(in_message)
    time.sleep(.25)
    if com:
        Popen(in_message,shell=True).communicate()
    else:
        Popen(in_message,shell=True)


def get_non_tied_mat(in_mat, epsilon = 1e-10):
    ## go through each column and see if the number of non-zeros is equal to the number of unique non-zeros
    for i in range(in_mat.shape[1]):
        bool_vect = in_mat[:,i]>0
        num_non_zero = np.sum(bool_vect)
        non_zero_vect = in_mat[bool_vect,i]
        print(num_non_zero,len(set(non_zero_vect)))
        if num_non_zero == len(set(non_zero_vect)):
            pass
        else:
            print("found",num_non_zero - len(set(non_zero_vect)),"ties at",i)
            in_mat[bool_vect,i] = in_mat[bool_vect,i] + np.random.randn(num_non_zero)*epsilon
    return(in_mat)


## taken from:
## https://github.com/ShawnLYU/Quantile_Normalize/blob/master/quantile_norm.py
def quantileNormalize(in_mat):
    ## takes in a numpy matrix
    in_mat = get_non_tied_mat(in_mat)
    df = pd.DataFrame(in_mat)
    #compute rank
    dic = {}
    for col in df:
        dic.update({col : sorted(df[col])})
    sorted_df = pd.DataFrame(dic)
    rank = sorted_df.mean(axis = 1).tolist()
    #sort
    for col in df:
        t = np.searchsorted(np.sort(df[col]), df[col])
        df[col] = [rank[i] for i in t]
    return(np.array(df))


def main(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    ## go through the file collecting the column headers, row ids, and non-zero information 
    first = True
    for line in fileinput.input(args.input_file):
        if first:
            first = False
            full_column_header = strip_split(line)## includes leader!
            ## set up  some of the other variables that we'll need for later lines
            sample_ids = full_column_header[1:]
            id_list = []
        else:
            id_list.append(strip_split(line)[0])
    fileinput.close()
    ## make the numpy array
    in_mat = np.zeros((len(id_list), len(sample_ids)))
    first = True
    counter = 0
    for line in fileinput.input(args.input_file):
        if first:
            first = False
        else:
            temp_line = strip_split(line)
            in_mat[counter,:] = temp_line[1:]
            counter += 1
    ## first figure out which columns need to be removed
    count_non_zero = np.sum(in_mat>0., axis = 0)
    #print(count_non_zero)
    ## figure out which samples didn't have enough expressed genes to keep.
    ## note the +1. This is because we will need to actually do the quantile
    ## normalization on the top n+1 genes, then subtract the minimum. Otherwise,
    ## there would be an abnormally large gap between 
    temp_keep_n = args.num_express+1
    keep_indices = np.where(count_non_zero >= temp_keep_n)[0]
    print("discarding",len(sample_ids)-keep_indices.shape[0],"samples because they didn't have enough detected genes")
    in_mat = in_mat[:,keep_indices]
    sample_ids = np.array(sample_ids)[keep_indices]
    sample_keep_mins = np.zeros((sample_ids.shape[0]))
    ## mask all of the places where it needs to be zero
    for i in range(sample_ids.shape[0]):
        temp_vect = in_mat[:,i]
        temp_lowest_cutoff = min(nlargest(temp_keep_n, temp_vect))
        temp_vect[np.where(temp_vect<temp_lowest_cutoff)[0]] = 0
        ## now we have to check for ties at the bottom & randomly drop out all but one
        n_need_to_remove = np.sum(temp_vect>0) - temp_keep_n
        #print(n_need_to_remove)
        if n_need_to_remove > 0:
            min_indices = np.where(temp_vect == temp_lowest_cutoff)[0]
            np.random.shuffle(min_indices)
            #print(min_indices)
            for j in range(n_need_to_remove):
                temp_vect[min_indices[j]] = 0
        #print(np.sum(temp_vect>0))
        in_mat[:,i] = temp_vect
    new_count_non_zero = np.sum(in_mat>0., axis = 0)
    print(new_count_non_zero)
    in_mat = quantileNormalize(in_mat)
    #in_mat = np.array(quantileNormalize(pd.DataFrame(in_mat)))
    ## figure out what that minimum value was
    first_col = in_mat[:,0]
    temp_min = min(first_col[first_col>0])
    print('temp_min is',temp_min)
    in_mat -= temp_min
    in_mat[in_mat<0] = 0
    temp_min = min(first_col[first_col>0])
    print('new temp_min is',temp_min)
    print('finished normalization\n\nwriting the output now')
    in_mat = in_mat.tolist()
    for i in range(len(in_mat)):
        in_mat[i] = [id_list[i]]+in_mat[i]
    in_mat = [["gene"]+sample_ids.tolist()] + in_mat
    write_table(in_mat, args.out_file)
    # in_mat = np.array(read_table(args.input_file), dtype = str)
    # in_mat_num = np.zeros((len(in_mat)-1,len(in_mat[0])-1),dtype = float)
    # in_mat = np.array(in_mat,dtype = 'U64')
    # for i in range(1,len(in_mat)-1):
    #     in_mat_num[i,:] = in_mat[i][1:]
    # in_mat_num = quantileNormalize(pd.DataFrame(in_mat_num))
    # in_mat[1:,1:]=np.array(in_mat_num)
    # write_table(in_mat,args.out_file)

if __name__ == "__main__":
    ##############################################################
    parser = argparse.ArgumentParser()

    parser.add_argument("-input_file", "-i","-infile",
        help="the input matrix")
    parser.add_argument("-out_file", "-o","-out",
        help="the output quantile normalized matrix")
    parser.add_argument("-num_express", "-n",
        type=int,
        help="the number of expressed genes")
    parser.add_argument("-seed",
        type=int,
        default = 123456,
        help="random seed to use - only pertient if there are ties in the dataset that need random breaking.")
    args = parser.parse_args()
    ##############################################################
    main(args)
