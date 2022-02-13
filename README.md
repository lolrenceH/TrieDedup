# TrieDedup


High-throughput sequencing is powerful and extensively applied in biological studies, although sequencers may report bases with low qualities and lead to ambiguous bases, 'N's. PCR duplicates introduced in library preparation need to be removed in genomics studies, and many deduplication tools have been developed for this purpose. However, the existing tools cannot deal with 'N's correctly or efficiently. Here we proposed and implemented TrieDedup, which uses trie (prefix tree) structure to compare and store sequences. TrieDedup can handle ambiguous base 'N's, and efficiently deduplicate at the level of raw sequences. We also reduced its memory usage by implementing restrictedListDict. We benchmarked the performance, and showed that TrieDedup can deduplicate reads up to 160X faster speed than pairwise comparison, with 36X higher memory usage.


Author : Jianqiao Hu & Adam Yongxin Ye @ BCH


# example workflow:
python TrieDedup.py --input input_seq_file >uniq_readIDs.txt
seqtk subseq input_seq_file uniq_readIDs.txt >uniq_seq_file

The format of input_seq_file will be automatically determined by the filename extension


Allowed extensions for input_seq_file include: .fasta .fa .fastq .fq

Additional arguments:
'--verbose', '-v': Print extra information to the error stream
'--input', '-i': 'The path to tje input file; can either be a fasta or a fastq file'
'--symbols', '-s': 'A string of expected characters in the input file; default is ACGTN.'
'--ambiguous', '-m': 'A string of characters that represent ambiguous bases; default is N; there can be more than one'
'--function', '-f': 'Speicify which deduplication algorithm to use; options include trie and pairwise
'--max_missing', 'N': 'The maxinum number of ambiguous characters allowed in a single read, for it to be considered';  default is 500
'--sorted': 'Use this option if the input file has been sorted by the number of Ns in each read'

