# TrieDedup: A fast trie-based deduplication algorithm to handle ambiguous bases in high-throughput sequencing

Background: High-throughput sequencing is a powerful tool that is extensively applied in biological studies. However, sequencers may produce low-quality bases, leading to ambiguous bases, 'N's. PCR duplicates introduced in library preparation should usually be removed in genomics studies, and several deduplication tools have been developed for this purpose. However, two identical reads may appear different due to ambiguous bases and the existing tools cannot address 'N's correctly or efficiently.

Results: Here we proposed and implemented TrieDedup, which uses trie (prefix tree) data structure to compare and store sequences. TrieDedup can handle ambiguous base 'N's, and efficiently deduplicate at the level of raw sequences. We also reduced its memory usage by approximately 20% by implementing restrictedDict in Python. We benchmarked the performance of the algorithm and showed that TrieDedup can deduplicate reads up to 270-fold faster than pairwise comparison at a cost of 32-fold higher memory usage. 

Conclusions: TrieDedup algorithm may facilitate PCR deduplication, barcode or UMI assignment and repertoire diversity analysis of large scale high-throughput sequencing datasets with its ultra-fast algorithm that can account for ambiguous bases due to sequencing errors.

Author: Adam Yongxin Ye & Jianqiao Hu @ Boston Children's Hospital / Harvard Medical School


## Implementation

- [Python version](https://github.com/lolrenceH/TrieDedup/tree/master/Python)
- [C++ version](https://github.com/lolrenceH/TrieDedup/tree/master/Cpp)
- [Java version](https://github.com/lolrenceH/TrieDedup/tree/master/Java)


## Wrapper

After you compile C++ code following its [README](https://github.com/lolrenceH/TrieDedup/tree/master/Cpp), you may use this simple top-level wrapper

> python TrieDedupWrapper.py
```
Usage: python this.py <implementation> <subcommand> <input>
	[output_format] [output] [max_missing] [sorted]

<implementation>	 one of 'cpp', 'java' or 'python'
<subcommand>    	 one of 'sortuniq', 'trie' or 'pairwise'
<input>         	 input *.fasta, *.fa, *.fastq or *.fq file
[output_format] 	 one of 'fasta', 'readID', 'sequence', 'dup2uniq', or 'uniq2dup' (default: fasta)
[output]        	 output filename (default: empty = STDOUT)
[max_missing]   	 max allowed ambiguous Ns per read (default: 9999)
[sorted]        	 is the input file has already been sorted by the number of Ns (default: False)
```

### Test example

> python TrieDedupWrapper.py python trie test_data/randomReads_1k_200bp.fasta fasta test_out.python_trie.fa

> python TrieDedupWrapper.py cpp trie test_data/randomReads_1k_200bp.fasta fasta test_out.cpp_trie.fa

> diff <(grep "^>" test_out.python_trie.fa | sort) <(grep "^>" test_out.cpp_trie.fa | sort)

Empty diff result means they output the same reads

### Note

When input ends in .fastq or .fq, python implementation will output in fastq format, while cpp and java implementation will output in fasta format


