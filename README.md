# TrieDedup: A fast trie-based deduplication algorithm to handle ambiguous bases in high-throughput sequencing

High-throughput sequencing is a powerful tool and is extensively applied in biological studies. However sequencers may report bases with low qualities and lead to ambiguous bases, 'N's. PCR duplicates introduced in library preparation need to be removed in genomics studies, and several deduplication tools have been developed for this purpose. However, the existing tools cannot deal with 'N's correctly or efficiently.

Here we proposed and implemented TrieDedup, which uses trie (prefix tree) structure to compare and store sequences. TrieDedup can handle ambiguous base 'N's, and efficiently deduplicate at the level of raw sequence reads. We also reduced its memory usage by implementing restrictedListDict. We benchmarked the performance of the algorithm and showed that TrieDedup can deduplicate reads up to 160X faster than pairwise comparison, but at a cost of 36X higher memory usage.

Author : Jianqiao Hu & Adam Yongxin Ye @ BCH

## Prerequisites

- python3
- [guppy3](https://github.com/zhuyifei1999/guppy3) (just for memory benchmarking)

## Usage

### Workflow

1. mask low quality bases (Q <= 10) by N  (need [seqtk](https://github.com/lh3/seqtk))
    >seqtk seq -Q33 -q10 -n N -i raw_seq.fq -o input_seq.fq

2. deduplicate a sequencing library using TrieDedup
    >python TrieDedup.py --input input_seq.fq >uniq_readIDs.txt

3. extract unique reads by their IDs  (need [seqtk](https://github.com/lh3/seqtk))
    >seqtk subseq input_seq.fq uniq_readIDs.txt >uniq_seq.fq

### Test example

> python3 TrieDedup.py -i SRR3744758_1_maskN_filtered_1k.fastq -v  >uniq_readIDs.txt

[NOTE]: Demultiplexing resulted in 920 unique reads. Time spent: 0.7362634092569351

> python3 TrieDedup.py -i SRR3744758_1_maskN_filtered_1k.fastq -v -f pairwise >uniq_readIDs.txt

[NOTE]: Demultiplexing resulted in 920 unique reads. Time spent: 1.543598547577858

### Detailed command-line usage document, and other arguments

> python3 TrieDedup.py -h
```
usage: TrieDedup.py [-h] [--verbose] --input INPUT [--symbols SYMBOLS]
                    [--ambiguous AMBIGUOUS] [--function FUNCTION]
                    [--max_missing N] [--sorted]

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         Print extra information to the error stream
  --input INPUT, -i INPUT
                        The path to tje input file; can either be a fasta or a
                        fastq file
  --symbols SYMBOLS, -s SYMBOLS
                        A string of expected characters in the input file;
                        default is ACGTN.
  --ambiguous AMBIGUOUS, -m AMBIGUOUS
                        A string of characters that represent ambiguous bases;
                        default is N; there can be more than one
  --function FUNCTION, -f FUNCTION
                        Use which function to deduplicate? [trie, pairwise]
  --max_missing N       The maxinum number of ambiguous characters allowed in
                        a single read, for it to be considered
  --sorted              Use this option if the input file has been sorted by
                        the number of Ns in each read
```


## Benchmark

### Usage example

> python3 benchmark.py -f trie --STARTING_FCT 0.01 --N_REGION_START 0 --N_REGION_END 1 --READ_LENGTH 10 --REGION_N_FCT 0.05 -i randomReads_100k_200bp_05182021.csv --random 3  >benchmark_output.txt

Note: input.csv only need one column of input sequences with colname "seq"

### Example output

>python3 benchmark.py -f trie --STARTING_FC 0.007692307692308 --N_REGION_START 0 --N_REGION_END 1 --READ_LENGTH 200 --REGION_N_FCT 0.01 -i randomReads_100k_200bp_05182021.csv  --random 1 -v --should_benchmark_memory

>[NOTE]: Starting with 0.007692307692308 of randomReads_100k_200bp_05182021.csv and inflating by 1.3

>[NOTE]: Inflated sample contain 558 unique reads

>[NOTE]: Masking 2.0 random bases in 0-200 region by N (0.01)

>[NOTE]: 1.0% of the 200bp reads is masked by N ACGTN

>[NOTE] Number of reads (raw) = 1000

>[NOTE] sorting...

>[NOTE]: Demultiplexing resulted in 558 unique reads. Time spent: 0.48185184597969055

\# example outputs


function | SAMPLE_SIZE | UNIQUE_SAMPLE | DEMULTIPLEXED_SAMPLE | READ_LENGTH | N_REGION | NUM_N | REGION_N_FCT | TOTAL_N_FCT | TIMESPENT | STARTING_FCT | INFLATION_FCT | SOURCE_READS | MEMORY_COST | i
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- 
trie | 1000 | 558 | 558 | 200 | [0.0, 1.0] | 2.0 | 0.01 | 0.01 | 0.48185184597969055 | 0.007692307692308 | 1.3 | randomReads_100k_200bp_05182021.csv | 0.09660495445132256 | 1

### Detailed command-line usage document, and additional arguments:

> python3 benchmark.py  -h
```
usage: benchmark.py [-h] [--STARTING_FCT STARTING_FCT]
                    [--INFLATION_FCT INFLATION_FCT]
                    [--N_REGION_START N_REGION_START]
                    [--N_REGION_END N_REGION_END]
                    [--REGION_N_FCT REGION_N_FCT] --READ_LENGTH READ_LENGTH
                    [--verbose] --input SOURCE_READS --function
                    TESTED_FUNCTION [--should_benchmark_memory]
                    [--symbols SYMBOLS] [--random RANDOM] [--print]

optional arguments:
  -h, --help            show this help message and exit
  --STARTING_FCT STARTING_FCT
                        Extract a fraction of reads from the source to use as
                        true unique reads
  --INFLATION_FCT INFLATION_FCT
                        Inflate the true unique reads by a specified factor
  --N_REGION_START N_REGION_START
                        The base position where Ns start being converted (from
                        0~1, where 0.5 would denote position 100 on a 200bp
                        long read)
  --N_REGION_END N_REGION_END
                        The base position where Ns stop being converted (from
                        0~1, where 0.5 would denote position 100 on a 200bp
                        long read)
  --REGION_N_FCT REGION_N_FCT
                        The percentage of bases that are converted to N in the
                        N region
  --READ_LENGTH READ_LENGTH
                        The length of reads in the input
  --verbose, -v         Print out helpful information
  --input SOURCE_READS, -i SOURCE_READS
                        The source reads that are uniform in length; a csv
                        file with a header of 'seq' and each row is a read
  --function TESTED_FUNCTION, -f TESTED_FUNCTION
                        The type of deduplication algorithm to use [pairwise,
                        trie]
  --should_benchmark_memory, -m
                        Whether to document memory usage
  --symbols SYMBOLS, -s SYMBOLS
                        The bases in the inputl; default = ACGTN
  --random RANDOM       Set a random seed
  --print               Whetehr to print out output
```

