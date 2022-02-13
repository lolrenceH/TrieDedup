# This is a command-line warpper for benchmark
# @Author : Jianqiao Hu & Adam Yongxin Ye @ BCH
"""
Usage example: python3 benchmark.py -f trie --STARTING_FCT 0.01 --N_REGION_START 0 --N_REGION_END 1 --READ_LENGTH 10 --REGION_N_FCT 0.05 -i benchmark/randomReads_100k_200bp_05182021.csv --random 3  >benchmark_output.txt

Note: input.csv only need one column of input sequences with colname "seq"
"""
import random
import argparse
import pandas as pd
import lib.pairwise
import lib.trie
from lib.restrictedDict import restrictedListDict

restrictedListDict.addAllowedKeys('ACGTN')

def parseArg():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--STARTING_FCT', default=0.01, type=float, help="Extract a fraction of reads from the source to use as true unique reads")
    parser.add_argument('--INFLATION_FCT', default=1.3, type=float, help="Inflate the true unique reads by a specified factor")
    parser.add_argument('--N_REGION_START', default=0, type=float, help="The base position where Ns start being converted (from 0~1, where 0.5 would denote position 100 on a 200bp long read)")
    parser.add_argument('--N_REGION_END', default=1, type=float, help="The base position where Ns stop being converted (from 0~1, where 0.5 would denote position 100 on a 200bp long read)")
    parser.add_argument('--REGION_N_FCT', default=0.3, type=float, help="The percentage of bases that are converted to N in the N region")
    parser.add_argument('--READ_LENGTH', type=int, required=True, help="The length of reads in the input")
    parser.add_argument('--verbose', '-v', default=False, action='store_true', help="Print out helpful information")
    parser.add_argument('--input', '-i', dest='SOURCE_READS', required=True, type=str, help="The source reads that are uniform in length; a csv file with a header of 'seq' and each row is a read")
    parser.add_argument('--function', '-f', dest='TESTED_FUNCTION', required=True, type=str, help="The type of deduplication algorithm to use [pairwise, trie]")
    parser.add_argument('--should_benchmark_memory', '-m', default=False, action='store_true', help="Whether to document memory usage")
    parser.add_argument('--symbols', '-s', dest='symbols', default='ACGTN', type=str, help="The bases in the inputl; default = ACGTN ")
    # 06172021 added print and ID options. print enables parallel running of multiple benchmark scripts whose outputs
    # are separated by > different file ### this does not work with tsp
    # 06182021 added add_mutually_exclusive_group such that you either specify repetitions or specify random states
    parser.add_argument('--random', default=1, type=int, help="Set a random seed")
    parser.add_argument('--print', default=True, action='store_true', help="Whetehr to print out output")
    # 06232021 added heap_mem_out: file path to where memory usage info will be written in byte unit
    args = parser.parse_args().__dict__
    args['N_REGION'] = [args['N_REGION_START'], args['N_REGION_END']]
    return args


def insertN(read, readLen, fctN, regionN=[0, 1]):
    read = read[:readLen]
    coord_regionN = [int(readLen * regionN[0]),
                     int(readLen * regionN[1])]  # the coordinates of the specific region of insertion
    regionLen = coord_regionN[1] - coord_regionN[0]  # the length of the insertion region

    numberN_float = fctN * regionLen  # number of Ns to be inserted into the region
    decimal = numberN_float % 1
    numberN = int(numberN_float)
    if decimal > 0:
        dice = random.random()
        if dice <= decimal:
            numberN = int(numberN_float) + 1
    N_positions = random.sample(range(coord_regionN[0], coord_regionN[1]), numberN)
    for pos in N_positions:
        read = read[:pos] + 'N' + read[pos + 1:]
    return read


def documentResults(param_dict, variable_set):
    # result = pd.read_csv(param_dict['result_path'], sep='\t')
    # new_row = pd.Series(index=variable_set, dtype=object)
    new_row = ''
    for var in variable_set:
        try:
            # new_row[var] = param_dict[var]
            new_row += str(param_dict[var]) + '\t'
            #
        except:
            print(f'[WARNING]: failed to log {eval(var)}')
    return new_row


def runRepeats(param_dict, i, inputReads):
    '''
    set up parameters --> mask reads by N with user specifications --> construct Trie and record time -->
    keep the unique reads only --> create a string that's to be documented --> append string to file through listener
    '''
    should_benchmark_memory = param_dict['should_benchmark_memory']
    function = param_dict['TESTED_FUNCTION']
    STARTING_FCT = param_dict['STARTING_FCT']
    INFLATION_FCT = param_dict['INFLATION_FCT']
    READ_LENGTH = param_dict['READ_LENGTH']
    N_REGION = param_dict['N_REGION']
    REGION_N_FCT = param_dict['REGION_N_FCT']
    if param_dict['verbose']:
        print(STARTING_FCT, INFLATION_FCT, READ_LENGTH, N_REGION, REGION_N_FCT)
    coord_regionN = [int(READ_LENGTH * N_REGION[0]), int(READ_LENGTH * N_REGION[1])]
    # setting up test df
    test = inputReads.sample(frac=STARTING_FCT, random_state=i)
    test_inflated = test.sample(frac=INFLATION_FCT, replace=True, random_state=i)
    SAMPLE_SIZE = len(test_inflated)
    UNIQUE_SAMPLE = len(test_inflated.drop_duplicates())
    if param_dict['verbose']:
        print(f'[NOTE]: Starting with {STARTING_FCT} of {param_dict["SOURCE_READS"]} and inflating by {INFLATION_FCT}')
        print(f'[NOTE]: Inflated sample contain {UNIQUE_SAMPLE} unique reads')
    # masking by N; added set seed for decimal Ns (1.5N has 50/50 chance to be 1 or 2)
    random.seed(i)
    test_inflated["seq"] = [insertN(seq, READ_LENGTH, REGION_N_FCT, N_REGION) for seq in test_inflated["seq"]]
    test_inflated = test_inflated.reset_index(drop=True)
    NUM_N = REGION_N_FCT * (coord_regionN[1] - coord_regionN[0])
    TOTAL_N_FCT = NUM_N / READ_LENGTH
    if param_dict['verbose']:
        print(f'[DEBUG] {test_inflated["seq"]}')
        print(f'[NOTE]: Masking {NUM_N} random bases in {coord_regionN[0]}-{coord_regionN[1]} region by N ({REGION_N_FCT})')
        print(f'[NOTE]: {TOTAL_N_FCT * 100}% of the {READ_LENGTH}bp reads is masked by N')
    # construct Trie and document time
    # write a list of bool values to indicate whether each sequence is unique or it has been seen

    if function == 'trie':
        ans_list = lib.trie.collapseSeq(test_inflated["seq"], param_dict, should_benchmark_memory=should_benchmark_memory, allowed_symbols=param_dict['symbols'],ambiguous_symbols=param_dict['ambiguous'])
    elif function == 'pairwise':
        ans_list = lib.pairwise.collapseSeq(test_inflated["seq"], should_benchmark_memory=should_benchmark_memory,max_missing=param_dict['N'])
    try:
        test_inflated['UNIQUE'] = ans_list[0]
    except ValueError:
        print('gdamn it')
    test_inflated_unique = test_inflated[test_inflated['UNIQUE'] == 1]
    DEMULTIPLEXED_SAMPLE = len(test_inflated_unique)
    TIMESPENT = ans_list[1]
    if should_benchmark_memory:
        # calculate memory usage and convert to gigabyte
        MEMORY_COST = str(ans_list[2].size/1024**3)

    if param_dict['verbose']:
        print(f'[NOTE]: Demultiplexing resulted in {DEMULTIPLEXED_SAMPLE} unique reads. Time spent: {TIMESPENT}')

    # 01192022 no need for ID column --> remove
    variable_set = ['function', 'SAMPLE_SIZE', 'UNIQUE_SAMPLE', 'DEMULTIPLEXED_SAMPLE', 'READ_LENGTH', 'N_REGION', 'NUM_N', 'REGION_N_FCT', 'TOTAL_N_FCT', 'TIMESPENT', 'STARTING_FCT', 'INFLATION_FCT', 'SOURCE_READS']
    if should_benchmark_memory:
        variable_set.append('MEMORY_COST')
    variable_set.append('i')
    for var in variable_set:
        if var not in param_dict:
            param_dict[var] = eval(var)
    res = documentResults(param_dict, variable_set)
    if param_dict['print']:
        print('\t'.join(variable_set), flush=True)
        print(res, flush=True)


def main():
    param_dict = parseArg()
    # put listener to work first
    # initialize input file
    SOURCE_READS = param_dict['SOURCE_READS']
    inputReads = pd.read_csv(SOURCE_READS)
    i = param_dict['random']
    runRepeats(param_dict, i, inputReads)
    # 06172021: added print option


if __name__ == '__main__':
    main()
