# TrieDedup (C++ implementation)

Author : Adam Yongxin Ye & Jianqiao Hu @ Boston Children's Hospital (BCH)


## Prerequisites

- g++


## Compilation

```
cd src

for prefix in ACGTNMap ACGTNTrieNode Deduper Main SeqIdAndSeq Timer; do
 echo $prefix
 echo g++ -std=c++0x -O2 -g3 -Wall -c -fmessage-length=0 -o $prefix.o $prefix.cpp
 time g++ -std=c++0x -O2 -g3 -Wall -c -fmessage-length=0 -o $prefix.o $prefix.cpp
done
prefix=YyxUtils; time g++ -std=c++0x -O2 -g3 -Wall -c -fmessage-length=0 -o $prefix.o $prefix.h

g++ -o TrieDedup ACGTNMap.o ACGTNTrieNode.o Deduper.o Main.o SeqIdAndSeq.o Timer.o 

[[ -f ./TrieDedup ]] && rm -f ./*.o

cd ..

mkdir bin

mv src/TrieDedup bin/TrieDedup

bin/TrieDedup
```


## Usage

### Detailed command-line usage document, and other arguments

> bin/TrieDedup
```
Usage: bin/TrieDedup
	 [options] <command> <input>
Options:
    -h|--help 			show this command-line help page
    -o|--output <file> 		set output file path (default: STDOUT)
    -s|--sorted 		input already uniq and sorted (default: false)
    -m|--max-missing <int> 	max number of Ns allowed for each read (default: 9999)
    -q|--min-baseQ <int> 	bases with lower baseQ will be converted to N (default: 0)
    -t|--baseQ-shift <int> 	baseQ value shifted from char (default: 33)
    -f|--output-format <str> 	output format [readID, sequence, fasta, dup2uniq, uniq2dup] (default: fasta)
Supported <command>:
    sortuniq 	just uniq by sequence and sort by N, and output fasta
    trie 	deduplicate using trie algorithm
    pairwise 	deduplicate using pairwise algorithm
Supported <input> format:
    (automatically determined by <input>'s file extension)
	.fasta, .fa, .fastq, .fq
Output:  STDOUT  or  -o|--output <file>
	format specified in -f|--output-format option
    If set to dup2uniq, I will output 4-column tsv format: 1st-2nd columns are original readID and sequences, 3rd-4th columns are the mapped deduplicated readID and sequences.
    If set to uniq2dup, I will output to STDOUT 5-column tsv format: 1st-2nd columns are deduplicated readID and sequences, 3rd column is frequency, 4th column is original readIDs concatenated by ',', 5th column is orignal sequences concatenated by ','.

Version: 0.1.1 (2024-03-12)
Author: Adam Yongxin Ye & Jianqiao Hu @ BCH
```


