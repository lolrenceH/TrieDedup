/*
 * SeqIdAndSeq.h
 *
 *  Created on: Jan 28, 2023
 *      Author: Adam Yongxin Ye @ BCH
 */

#ifndef SEQIDANDSEQ_H_
#define SEQIDANDSEQ_H_

#include <vector>
#include <string>
#include <cstdio>

typedef std::pair<std::string, std::string> SeqIdAndSeq;

void write_fasta(std::ostream *out, std::vector<SeqIdAndSeq> id_seqs);

std::vector<SeqIdAndSeq> read_fasta(std::string input_path);
std::vector<SeqIdAndSeq> read_fastq(std::string input_path, int min_baseQ, int baseQ_coding_shift);

#endif /* SEQIDANDSEQ_H_ */
