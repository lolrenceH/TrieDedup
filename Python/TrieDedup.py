#!/usr/bin/env python3

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


def parseArg():
    parser = argparse.ArgumentParser(add_help=True, epilog='''
If --output_format is set to dup2uniq, I will output to STDOUT 4-column tsv format: 1st-2nd columns are original readID and sequences, 3rd-4th columns are the mapped deduplicated readID and sequences.  
If --output_format is set to uniq2dup, I will output to STDOUT 5-column tsv format: 1st-2nd columns are deduplicated readID and sequences, 3rd column is frequency, 4th column is original readIDs concatenated by ',', 5th column is orignal sequences concatenated by ','.
''')
    parser.add_argument('--verbose', '-v', default=False, action='store_true',
                        help='Print extra information to the error stream')
    parser.add_argument('--input', '-i', dest='input', type=str, required=True,
                        help='The path to the input file; can either be a fasta or a fastq file')
    parser.add_argument('--symbols', '-s', dest='symbols', default='ACGTN', type=str,
                        help='A string of expected characters in the input file; default is ACGTN.')
    parser.add_argument('--ambiguous', '-m', dest='ambiguous', default='N', type=str,
                        help='A string of characters that represent ambiguous bases; default is N; there can be more than one')
    parser.add_argument('--function', '-f', default='trie', type=str,
                        help='Use which function to deduplicate? [sortuniq, trie, pairwise]')
    parser.add_argument('--max_missing', '-N', dest='N', default=500, type=int,
                        help='The maxinum number of ambiguous characters allowed in a single read, for it to be considered')
    parser.add_argument('--sorted', default=False, action="store_true",
                        help='Use this option if the input file has been sorted by the number of Ns in each read')
    parser.add_argument('--output_format', '-o', default='readID', type=str,
                        help='Output format of STDOUT; default is readID [readID, sequence, fasta, dup2uniq, uniq2dup]')
    args = parser.parse_args().__dict__
    return args


def check_seqFile_type(input_path):
    split_tup = os.path.splitext(input_path)
    file_extension = split_tup[1]
    if file_extension == ".fastq" or file_extension == ".fq":
        return "fastq"
    elif file_extension == ".fasta" or file_extension == ".fa":
        return "fasta"
    elif file_extension == ".txt" or file_extension == ".csv" or file_extension == ".tsv" or file_extension == ".list":
        return "text"
    else:
        raise FileNotFoundError(f"[ERROR]: Cannot determine the extension of {input_path}; Please specify with --type")


def read_fasta(input_path):
    names_vec = []
    seqs_vec = []
    now_name = ''
    now_seq = ''
    with open(input_path, 'r') as infile:
        for line in infile:
            line = line.rstrip()
            if line[0] == '>':
                if now_name != '':
                    names_vec.append(now_name.split(" ")[0])
                    seqs_vec.append(now_seq)
                now_name = line[1:]
                now_seq = ''
            else:
                now_seq += line
        if now_name != '':
            names_vec.append(now_name.split(" ")[0])
            seqs_vec.append(now_seq)
    return names_vec, seqs_vec


def read_fastq(input_path):
    names_vec = []
    seqs_vec = []
    now_name = ''
    with open(input_path, 'r') as infile:
        NR = 0
        for line in infile:
            NR += 1
            line = line.rstrip()
            if NR % 4 == 1:
                now_name = ''
                if line[0] == '@':
                    now_name = line[1:]
                elif len(line) > 0:
                    print(f'Warning: {NR}-th line does not start with @, invalid fastq format', file=sys.stderr)
            elif NR % 4 == 2:
                if now_name != '':
                    names_vec.append(now_name.split(" ")[0])
                    seqs_vec.append(line)
    return names_vec, seqs_vec


def read_text(input_path):
    names_vec = []
    seqs_vec = []
    with open(input_path, 'r') as infile:
        NR = 0
        for line in infile:
            NR += 1
            line = line.rstrip()
            if NR == 1 and line == 'seq':  # skip headline of colname 'seq'
                continue
            names_vec.append(str(NR))
            seqs_vec.append(line)
    return names_vec, seqs_vec


def read_input(input_reads, param_dict):
    """
    :param input_reads: path to the input sequencing file
    :param param_dict: param_dict
    :return: a pd.DataFrame sorted by number of Ns, containing 3 columns ['name', 'query', 'num_N']
    """
    input_type = check_seqFile_type(input_reads)
    # build pd.df of input
    names_ls = []
    query_ls = []
    if input_type == 'fasta':
        names_ls, query_ls = read_fasta(input_reads)
    elif input_type == 'fastq':
        names_ls, query_ls = read_fastq(input_reads)
    elif input_type == 'text':
        names_ls, query_ls = read_text(input_reads)
    #    SeqIO_parser = SeqIO.parse(open(input_reads), input_type)
    #    for read in SeqIO_parser:
    #        name, query = read.id, str(read.seq)
    #        names_ls.append(name)
    #        query_ls.append(query)
    input_df = pd.DataFrame({'name': names_ls, 'query': query_ls})
    input_df["num_N"] = [seq.count('N') for seq in input_df['query']]
    if not param_dict['sorted']:
        input_df_sort = input_df.sort_values(by=['num_N'])
        input_df_sort = input_df_sort.reset_index(drop=True)
    if param_dict['verbose']:
        input_row_col = input_df_sort.shape
        print(f"[LOG] Reading in {input_reads}", file=sys.stderr)
        print(f"[LOG] Number of raw reads = {input_row_col[0]}", file=sys.stderr)
    if param_dict['N'] is not None:
        input_df_sort = input_df_sort[input_df_sort["num_N"] <= param_dict['N']]
        input_row_col = input_df_sort.shape
        print(f"[LOG] Number of raw reads that have {param_dict['N']} N or less = {input_row_col[0]}", file=sys.stderr)
    return input_df_sort
    # return input_df


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
    output_format = param_dict['output_format']
    should_traceback = output_format == 'dup2uniq' or output_format == 'uniq2dup'
    if param_dict['verbose']:
        print(f'[NOTE] Start deduplicating using {function} algorithm', file=sys.stderr)
    # start deduplication
    if function == 'sortuniq':
        ans_list = lib.trie.collapseSeq(input_df_sort['query'], allowed_symbols=param_dict['symbols'],
                                        ambiguous_symbols=param_dict['ambiguous'], is_input_sorted=param_dict['sorted'],
                                        max_missing=param_dict['N'], should_just_uniq_sort=True, should_traceback=should_traceback)
    elif function == 'trie':
        ans_list = lib.trie.collapseSeq(input_df_sort['query'], allowed_symbols=param_dict['symbols'],
                                        ambiguous_symbols=param_dict['ambiguous'], is_input_sorted=param_dict['sorted'],
                                        max_missing=param_dict['N'], should_traceback=should_traceback)
    elif function == 'pairwise':
        ans_list = lib.pairwise.collapseSeq(input_df_sort['query'], max_missing=param_dict['N'], should_traceback=should_traceback)
#    input_df_sort["unqiue"] = ans_list[0]
    time_spent = ans_list[1]
    ans_vec = ans_list[0]
    # end deduplication
    num_dedup = 0
    if should_traceback:
        if output_format == 'dup2uniq':
            uniqIdx2idxes = dict()
            for idx, uniqIdx in enumerate(ans_vec):
                uniqIdx2idxes[uniqIdx] = 1
                orig_readID = input_df_sort.at[idx, 'name']
                orig_seq = input_df_sort.at[idx, 'query']
                if uniqIdx >= 0:
                    uniq_readID = input_df_sort.at[uniqIdx, 'name']
                    uniq_seq = input_df_sort.at[uniqIdx, 'query']
                else:
                    uniq_readID = '(filtered out, probably too many Ns)'
                    uniq_seq = '(filtered out, probably too many Ns)'
                print(f'{orig_readID}\t{orig_seq}\t{uniq_readID}\t{uniq_seq}')
        if output_format == 'uniq2dup':
            uniqIdx2idxes = dict()
            for idx, uniqIdx in enumerate(ans_vec):
                if uniqIdx >= 0:
                    if uniqIdx not in uniqIdx2idxes:
                        uniqIdx2idxes[uniqIdx] = []
                    uniqIdx2idxes[uniqIdx].append(idx)
            for uniqIdx, idxes in uniqIdx2idxes.items():
                uniq_readID = input_df_sort.at[uniqIdx, 'name']
                uniq_seq = input_df_sort.at[uniqIdx, 'query']
                now_count = len(idxes)
                orig_readIDs = ','.join([input_df_sort.at[x, 'name'] for x in idxes])
                orig_seqs = ','.join([input_df_sort.at[x, 'query'] for x in idxes])
                print(f'{uniq_readID}\t{uniq_seq}\t{now_count}\t{orig_readIDs}\t{orig_seqs}')
        num_dedup = len(list(uniqIdx2idxes.keys()))
    else:
        for idx in ans_vec:
#            print(f'idx={idx}', file=sys.stderr)
            readID = input_df_sort.at[idx, 'name']
            seq = input_df_sort.at[idx, 'query']
            if output_format == 'fasta':
                print(f">{readID}\n{seq}")
            elif output_format == 'readID':
                print(readID)
            elif output_format == 'sequence':
                print(seq)
            num_dedup += 1
    if param_dict['verbose']:
        print(f'[NOTE] Deduplicating resulted in {num_dedup} unique reads. Time spent: {time_spent} s', file=sys.stderr)


if __name__ == '__main__':
    main()
