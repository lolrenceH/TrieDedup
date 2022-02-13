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

'--STARTING_FCT': "Extract a fraction of reads from the source to use as true unique reads; required; set to 0 if not needed"					

'--INFLATION_FCT': "Inflate the true unique reads by a specified factor; required; set to 0 if not needed"

'--N_REGION_START': "The base position where Ns start being converted (from 0~1: where 0.5 would denote position 100 on a 200bp long read; required; set to 0 if no need to convert Ns)"

'--N_REGION_END': "The base position where Ns stop being converted (from 0~1: where 0.5 would denote position 100 on a 200bp long read; required; set to 0 if no need to convert Ns)"

'--REGION_N_FCT': "The percentage of bases that are converted to N in the N region; required"

'--READ_LENGTH': "The length of reads in the input; required"

'--verbose', '-v': "Print out helpful information"

'--input', '-i': "The source reads that are uniform in length; a csv file with a header of 'seq' and each row is a read; required"

'--function', '-f': "The type of deduplication algorithm to use. options = [pairwise, trie]; required"

'--should_benchmark_memory', '-m': "Whether to document memory usage"

'--random': "Set a random seed"

'--print': "Whetehr to print out output"
