# TrieDedup (Java implementation)

Author : Adam Yongxin Ye & Jianqiao Hu @ Boston Children's Hospital (BCH)


## Usage

### Detailed command-line usage document, and other arguments

> java -jar TrieDedup.jar
```
Usage: java -jar TrieDedup.jar <command> <input>

Version: 0.1.2 (2022-10-21)
Author: Adam Yongxin Ye & Jianqiao Hu @ BCH

Supported <command>:
    sortuniq
               just uniq by sequence and sort by N, and output fasta
    trie
               deduplicate using trie algorithm
    pairwise
               deduplicate using pairwise algorithm

Supported <input> format:
    (automatically determined by <input>'s file extension)
               .fasta, .fa,  .fastq, .fq,  .sam, .bam, .cram

Output:  STDOUT  or  -o|--output <file>
               in fasta format

Options:
 -h,--help                show this command-line help page
 -m,--max-missing <int>   max number of Ns allowed for each read (default:
                          9999)
 -o,--output <file>       set output file path (default: STDOUT)
 -q,--min-baseQ <int>     bases with lower baseQ will be converted to N
                          (default: 0)
 -s,--sorted              input already uniq and sorted (default: false)
 -t,--baseQ-shift <int>   baseQ value shifted from char (default: 33)
```


