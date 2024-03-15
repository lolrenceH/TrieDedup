# TrieDedup (Python implementation)

Author : Jianqiao Hu & Adam Yongxin Ye @ Boston Children's Hospital (BCH)


## Prerequisites

- python3
- [pandas](https://pandas.pydata.org/docs/getting_started/install.html)
- [guppy3](https://github.com/zhuyifei1999/guppy3) (just for memory benchmarking)
- [seqtk](https://github.com/lh3/seqtk)

## Usage

### Workflow

1. mask low quality bases (Q <= 10) by N  (need [seqtk](https://github.com/lh3/seqtk))
    >seqtk seq -Q33 -q10 -n N -i raw_seq.fq -o input_seq.fq

2. deduplicate a sequencing library using TrieDedup
    >python TrieDedup.py --input input_seq.fq >uniq_readIDs.txt

3. extract unique reads by their IDs  (need [seqtk](https://github.com/lh3/seqtk))
    >seqtk subseq input_seq.fq uniq_readIDs.txt >uniq_seq.fq

Alternatively, you can specify option --output_format, like

> python TrieDedup.py --input input_seq.fq --output_format fasta >uniq_seq.fa

### Test example

> python3 TrieDedup.py -i ../test_data/SRR3744758_1_maskN_filtered_1k.fastq -v  >uniq_readIDs.txt

Note: equivalent to also adding the optional argument '-f trie', which is default

```
[LOG] Reading in ../test_data/SRR3744758_1_maskN_filtered_1k.fastq
[LOG] Number of raw reads = 1000
[LOG] Number of raw reads that have 500 N or less = 1000
[NOTE] Start deduplicating using trie algorithm
[NOTE] Number of reads (raw) = 1000
[NOTE] Number of reads (filtering out exact matches) = 992
[NOTE] sorting...
[NOTE] Number of reads (filtering out exact matches) that have 500 N or less = 992
[NOTE] Deduplicating resulted in 920 unique reads. Time spent: 0.779429204761982 s
```

> python3 TrieDedup.py -i ../test_data/SRR3744758_1_maskN_filtered_1k.fastq -v -f pairwise >uniq_readIDs.txt

```
[LOG] Reading in ../test_data/SRR3744758_1_maskN_filtered_1k.fastq
[LOG] Number of raw reads = 1000
[LOG] Number of raw reads that have 500 N or less = 1000
[NOTE] Start deduplicating using pairwise algorithm
[NOTE] Deduplicating resulted in 920 unique reads. Time spent: 1.5659185945987701 s
```

The output numbers should be the same, except for the time, which may vary depending on your machine

### Detailed command-line usage document, and other arguments

> python3 TrieDedup.py -h
```
usage: TrieDedup.py [-h] [--verbose] --input INPUT [--symbols SYMBOLS]
                    [--ambiguous AMBIGUOUS] [--function FUNCTION]
                    [--max_missing N] [--sorted]
                    [--output_format OUTPUT_FORMAT]

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         Print extra information to the error stream
  --input INPUT, -i INPUT
                        The path to the input file; can either be a fasta or a
                        fastq file
  --symbols SYMBOLS, -s SYMBOLS
                        A string of expected characters in the input file;
                        default is ACGTN.
  --ambiguous AMBIGUOUS, -m AMBIGUOUS
                        A string of characters that represent ambiguous bases;
                        default is N; there can be more than one
  --function FUNCTION, -f FUNCTION
                        Use which function to deduplicate? [sortuniq, trie,
                        pairwise]
  --max_missing N, -N N
                        The maxinum number of ambiguous characters allowed in
                        a single read, for it to be considered
  --sorted              Use this option if the input file has been sorted by
                        the number of Ns in each read
  --output_format OUTPUT_FORMAT, -o OUTPUT_FORMAT
                        Output format of STDOUT; default is readID [readID,
                        sequence, fasta, dup2uniq, uniq2dup]

If --output_format is set to dup2uniq, I will output to STDOUT 4-column tsv
format: 1st-2nd columns are original readID and sequences, 3rd-4th columns are
the mapped deduplicated readID and sequences. If --output_format is set to
uniq2dup, I will output to STDOUT 5-column tsv format: 1st-2nd columns are
deduplicated readID and sequences, 3rd column is frequency, 4th column is
original readIDs concatenated by ',', 5th column is orignal sequences
concatenated by ','.
```


## Benchmark

### Usage example

#### Benchmark running time

> python3 benchmark.py -f trie --STARTING_FCT 0.8 --N_REGION_START 0 --N_REGION_END 1 --READ_LENGTH 200 --REGION_N_FCT 0.05 -i ../test_data/randomReads_1k_200bp.csv --random 3 -v  >benchmark_output.txt

```
[NOTE] Starting with 0.8 of ../test_data/randomReads_1k_200bp.csv and inflating by 1.3
[NOTE] Inflated sample contain 574 unique reads
[NOTE] Masking 10.0 random bases in 0-200 region by N (0.05)
[NOTE] 5.0% of the 200bp reads is masked by N ACGTN
[NOTE] Number of reads (raw) = 1040
[NOTE] sorting...
[NOTE] Demultiplexing resulted in 574 unique reads. Time spent: 0.3654523342847824 s
```


#### Benchmark memory usage

>python3 benchmark.py -f trie --STARTING_FC 0.8 --N_REGION_START 0 --N_REGION_END 1 --READ_LENGTH 200 --REGION_N_FCT 0.05 -i ../test_data/randomReads_1k_200bp.csv --random 3 -v --should_benchmark_memory  >benchmark_output.txt

```
[NOTE] Starting with 0.8 of ../test_data/randomReads_1k_200bp.csv and inflating by 1.3
[NOTE] Inflated sample contain 574 unique reads
[NOTE] Masking 10.0 random bases in 0-200 region by N (0.05)
[NOTE] 5.0% of the 200bp reads is masked by N ACGTN
[NOTE] Number of reads (raw) = 1040
[NOTE] sorting...
[NOTE] Demultiplexing resulted in 574 unique reads. Time spent: 0.40281282365322113 s
```

> less benchmark_output.txt

```
function        SAMPLE_SIZE     UNIQUE_SAMPLE   DEMULTIPLEXED_SAMPLE    READ_LENGTH     N_REGION        NUM_N   REGION_N_FCT    TOTAL_N_FCT     TIMESPENT       STARTING_FCT    INFLATION_FCT   SOURCE_READS    MEMORY_COST     i
trie    1040    574     574     200     [0.0, 1.0]      10.0    0.05    0.05    0.40281282365322113     0.8     1.3     ../test_data/randomReads_1k_200bp.csv   0.05796102527529001     3
```

### Detailed command-line usage document, and additional arguments:

> python3 benchmark.py -h
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
                        The length of query reads (can be less or equal to the
                        length in the input)
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

Note: input.csv only need one column of input sequences with colname "seq"
