/*
 * Deduper.h
 *
 *  Created on: Jan 29, 2023
 *      Author: Adam Yongxin Ye @ BCH
 */

#ifndef DEDUPER_H_
#define DEDUPER_H_

#include "SeqIdAndSeq.h"

int countN(SeqIdAndSeq id_seq);

bool compareN(SeqIdAndSeq i1, SeqIdAndSeq i2);

class Deduper {
public:
	Deduper();
	virtual ~Deduper();

	static std::vector<SeqIdAndSeq> uniq_and_sort(std::vector<SeqIdAndSeq> id_seqs, bool is_input_sorted, int max_missing);
	static std::vector<SeqIdAndSeq> collapseSeqTrie(std::vector<SeqIdAndSeq> uniq_id_seqs);

	static bool checkSeqEqual(std::string seq1, std::string seq2);
	static std::vector<SeqIdAndSeq> collapseSeqPairwise(std::vector<SeqIdAndSeq> uniq_id_seqs);
};

#endif /* DEDUPER_H_ */
