# This is a simple command-line wrapper of TrieDedup
# @Author : Jianqiao Hu & Adam Yongxin Ye @ BCH
"""
Usage:
python TrieDedup.py --input input_seq_file -v >uniq_readIDs.txt
seqtk subseq input_seq_file uniq_readIDs.txt >uniq_seq_file

The format of input_seq_file will be automatically determined by the filename extension
Allowed extensions include: .fasta .fa .fastq .fq
"""

import sys
import os
import argparse
import timeit
import pandas as pd
import lib.pairwise
import lib.trie
from lib.restrictedDict import restrictedListDict
from Bio import SeqIO


def parseArg():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--verbose', '-v', default=False, action='store_true',help='Print extra information to the error stream')
    parser.add_argument('--input', '-i', dest='input', type=str, required=True, help='The path to tje input file; can either be a fasta or a fastq file')
    parser.add_argument('--symbols', '-s', dest='symbols', default='ACGTN', type=str, help='A string of expected characters in the input file; default is ACGTN.')
    parser.add_argument('--ambiguous', '-m', dest='ambiguous', default='N', type=str, help='A string of characters that represent ambiguous bases; default is N; there can be more than one')
    parser.add_argument('--function', '-f', default='trie', type=str,help='Use which function to deduplicate? [trie, pairwise]')
    parser.add_argument('--max_missing', dest='N', default=500, type=int, help='The maxinum number of ambiguous characters allowed in a single read, for it to be considered')
    parser.add_argument('--sorted', default=False, action="store_true",help='Use this option if the input file has been sorted by the number of Ns in each read')
    args = parser.parse_args().__dict__
    return args


def check_seqFile_type(input_path):
    split_tup = os.path.splitext(input_path)
    file_extension = split_tup[1]
    if file_extension == ".fastq" or file_extension == ".fq":
        return "fastq"
    elif file_extension == ".fasta" or file_extension == ".fa":
        return "fasta"
    else:
        raise FileNotFoundError(f"[ERROR]: Cannot determine the extension of {input_path}; Please specify with --type")


def read_input(input_reads, param_dict):
    """
    :param input_reads: path to the input sequencing file
    :param param_dict: param_dict
    :return: a pd.DataFrame sorted by number of Ns, containing 3 columns ['name', 'query', 'num_N']
    """
    input_type = check_seqFile_type(input_reads)
    SeqIO_parser = SeqIO.parse(open(input_reads), input_type)
    # build pd.df of input
    names_ls = []
    query_ls = []
    for read in SeqIO_parser:
        name, query = read.id, str(read.seq)
        names_ls.append(name)
        query_ls.append(query)
    input_df = pd.DataFrame({'name': names_ls, 'query': query_ls})
    #input_df["num_N"] = [seq.count('N') for seq in input_df['query']]
    #input_df_sort = input_df.sort_values(by=['num_N'])
    #input_df_sort = input_df_sort.reset_index(drop=True)
    #if param_dict['verbose']:
    #    input_row_col = input_df_sort.shape
    #    print(f"[LOG] Reading in {input_reads}", file=sys.stderr)
    #    print(f"[LOG] Number of raw reads = {input_row_col[0]}", file=sys.stderr)
    #if param_dict['N'] is not None:
    #    input_df_sort = input_df_sort[input_df_sort["num_N"] <= param_dict['N']]
    #    input_row_col = input_df_sort.shape
    #    print(f"[LOG] Number of raw reads that have {param_dict['N']} N or less = {input_row_col[0]}", file=sys.stderr)
    #return input_df_sort
    return input_df


def main():
    """
    set up parameters --> mask reads by N with user specifications --> construct Trie and record time -->
    keep the unique reads only --> create a string that's to be documented --> append string to file through listener
    """
    # read in arguments
    param_dict = parseArg()
    # read in input
    input_reads = param_dict['input']
    input_df_sort = read_input(input_reads, param_dict)
    # start timer
    function = param_dict['function']
    # start deduplication
    if function == 'trie':
        ans_list = lib.trie.collapseSeq(input_df_sort['query'], allowed_symbols=param_dict['symbols'],ambiguous_symbols=param_dict['ambiguous'],is_input_sorted = param_dict['sorted'], max_missing=param_dict['N'])

    elif function == 'pairwise':
        ans_list = lib.pairwise.collapseSeq(input_df_sort['query'],max_missing=param_dict['N'])
    input_df_sort["unqiue"] = ans_list[0]
    time_spent = ans_list[1]
    # end deduplication
    dup_id = list(input_df_sort["name"][input_df_sort["unqiue"]==0])
    unique_id = list(input_df_sort["name"][input_df_sort["unqiue"]==1])
    num_dedup = len(unique_id)
    num_dup = len(dup_id)
    for u_id in unique_id:
        print(u_id)
    if param_dict['verbose']:
        print(f'[NOTE]: Demultiplexing resulted in {num_dedup} unique reads. Time spent: {time_spent}', file=sys.stderr)


if __name__ == '__main__':
    main()
