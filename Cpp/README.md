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
Supported <command>:
    sortuniq 	just uniq by sequence and sort by N, and output fasta
    trie 	deduplicate using trie algorithm
    pairwise 	deduplicate using pairwise algorithm
Supported <input> format:
    (automatically determined by <input>'s file extension)
	.fasta, .fa, .fastq, .fq
Output:  STDOUT  or  -o|--output <file>
	in fasta format

Version: 0.1.0 (2023-01-30)
Author: Adam Yongxin Ye & Jianqiao Hu @ BCH
```


