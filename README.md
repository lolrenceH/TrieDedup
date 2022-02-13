# TrieDedup - abstract


High-throughput sequencing is powerful and extensively applied in biological studies, although sequencers may report bases with low qualities and lead to ambiguous bases, 'N's. PCR duplicates introduced in library preparation need to be removed in genomics studies, and many deduplication tools have been developed for this purpose. However, the existing tools cannot deal with 'N's correctly or efficiently. Here we proposed and implemented TrieDedup, which uses trie (prefix tree) structure to compare and store sequences. TrieDedup can handle ambiguous base 'N's, and efficiently deduplicate at the level of raw sequences. We also reduced its memory usage by implementing restrictedListDict. We benchmarked the performance, and showed that TrieDedup can deduplicate reads up to 160X faster speed than pairwise comparison, with 36X higher memory usage.


Author : Jianqiao Hu & Adam Yongxin Ye @ BCH


# TrieDedup - example Linux bash workflow:

\# mask low quality bases (Q <= 10) by N 

fastq_masker -Q 33 -q 10 -r N -i raw_seq_file -o input_seq_file


\# deduplicate a sequencing library using TrieDedup

python TrieDedup.py --input input_seq_file >uniq_readIDs.txt


\# extract unique reads by their IDs 

seqtk subseq input_seq_file uniq_readIDs.txt >uniq_seq_file



# TrieDedup - Additional arguments:
'--verbose', '-v': Print extra information to the error stream

'--input', '-i': 'The path to the input file; can either be a fasta or a fastq file. The format of input_seq_file will be automatically determined by the filename extension. Allowed extensions for input_seq_file include: .fasta .fa .fastq .fq'

'--symbols', '-s': 'A string of expected characters in the input file; default is ACGTN.'

'--ambiguous', '-m': 'A string of characters that represent ambiguous bases; default is N; there can be more than one such characters'

'--function', '-f': 'Speicify which deduplication algorithm to use; options include trie and pairwise

'--max_missing', 'N': 'The maxinum number of ambiguous characters allowed in a single read, for it to be considered';  default is 500

'--sorted': 'Use this option if the input file has been sorted by the number of Ns in each read'


# TrieDedup - Benchmarking:
Usage example: python3 benchmark.py -f trie --STARTING_FCT 0.01 --N_REGION_START 0 --N_REGION_END 1 --READ_LENGTH 10 --REGION_N_FCT 0.05 -i randomReads_100k_200bp_05182021.csv --random 3  >benchmark_output.txt
Note: input.csv only need one column of input sequences with colname "seq"


'--STARTING_FCT', default=0.01, type=float)
    parser.add_argument('--INFLATION_FCT', default=1.3, type=float)
    parser.add_argument('--N_REGION_START', default=0, type=float)
    parser.add_argument('--N_REGION_END', default=1, type=float)
    parser.add_argument('--REGION_N_FCT', default=0.3, type=float)
    parser.add_argument('--READ_LENGTH', default=500, type=int)
    parser.add_argument('--verbose', '-v', default=False, action='store_true')
    parser.add_argument('--input', '-i', dest='SOURCE_READS', required=True, type=str)
    parser.add_argument('--function', '-f', dest='TESTED_FUNCTION', required=True, type=str)
    parser.add_argument('--should_benchmark_memory', '-m', default=False, action='store_true')
    parser.add_argument('--symbols', '-s', dest='symbols', default='ACGTN', type=str)
    # 06172021 added print and ID options. print enables parallel running of multiple benchmark scripts whose outputs
    # are separated by > different file ### this does not work with tsp
    # 06182021 added add_mutually_exclusive_group such that you either specify repetitions or specify random states
    parser.add_argument('--random', default=1, type=int)
    parser.add_argument('--print', default=True, action='store_true')
    # 06232021 added heap_mem_out: file path to where memory usage info will be written in byte unit
    args = parser.parse_args().__dict__
    args['N_REGION'] = [args['N_REGION_START'], args['N_REGION_END']]
