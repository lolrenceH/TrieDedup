/*
 * Deduper.cpp
 *
 *  Created on: Jan 29, 2023
 *      Author: Adam Yongxin Ye @ BCH
 */

#include <iostream>
#include <unordered_map>
#include <string>
#include <algorithm>

#include "Deduper.h"
#include "YyxUtils.h"
#include "Timer.h"
#include "ACGTNTrieNode.h"
//#include "SeqIdAndSeq.h"

int countN(SeqIdAndSeq id_seq){
	int count = 0;
	for(unsigned int i=0; i<id_seq.second.length(); i++){
		if(id_seq.second[i] == 'N'){
			count++;
		}
	}
	return count;
}

// reference: https://www.geeksforgeeks.org/sort-c-stl/
bool compareN(SeqIdAndSeq i1, SeqIdAndSeq i2){
	return (countN(i1) < countN(i2));
}


Deduper::Deduper() {
}

Deduper::~Deduper() {
}

std::vector<SeqIdAndSeq> Deduper::uniq_and_sort(std::vector<SeqIdAndSeq> id_seqs, bool is_input_sorted, int max_missing){
	std::cerr << string_format("[NOTE] Number of reads (raw) = %d", id_seqs.size()) << std::endl;
	Timer tm;
	std::unordered_map<std::string, bool> uniq_seqs_hash;
	std::vector<SeqIdAndSeq> uniq_id_seqs;
	int lastCountN = -1;
	int currentCountN;
	std::cerr << "[STEP] uniqueing and filtering out sequences with too many Ns ..." << std::endl;
	for(unsigned int k=0; k<id_seqs.size(); k++){
		SeqIdAndSeq id_seq = id_seqs[k];
//	for(SeqIdAndSeq id_seq : id_seqs){
		// reference: https://stackoverflow.com/questions/14159682/unordered-map-which-one-is-faster-find-or-count
		if(uniq_seqs_hash.count(id_seq.second) == 0){
			uniq_seqs_hash[id_seq.second] = true;
			currentCountN = countN(id_seq);
			if(is_input_sorted){
				if(currentCountN < lastCountN){
					std::cerr << "Warning: some later sequence has fewer Ns than previous sequence, which violates the assumption of sorted input, so I will set is_input_sorted = false instead" << std::endl;
					is_input_sorted = false;
				}else{
					lastCountN = currentCountN;
				}
			}
			if(currentCountN <= max_missing){
				uniq_id_seqs.push_back(id_seq);
			}else if(is_input_sorted){
				break;
			}
		}
	}
	std::cerr << " \t" << tm.format_elapsed_time() << std::endl;
	std::cerr << string_format("[NOTE] Number of reads (filtered out too many Ns) = %d", uniq_id_seqs.size()) << std::endl;

	if(! is_input_sorted){
		std::cerr << "[STEP] sorting ..." << std::endl;
		tm.reset();
		// reference: https://www.geeksforgeeks.org/sorting-a-vector-in-c/
		std::sort(uniq_id_seqs.begin(), uniq_id_seqs.end(), compareN);
	}
	return uniq_id_seqs;
}

std::vector<SeqIdAndSeq> Deduper::collapseSeqTrie(std::vector<SeqIdAndSeq> uniq_id_seqs){
	std::vector<SeqIdAndSeq> dedup_id_seqs;

	ACGTNTrieNode trie;
	for(unsigned int k=0; k<uniq_id_seqs.size(); k++){
		SeqIdAndSeq id_seq = uniq_id_seqs[k];
//	for(SeqIdAndSeq id_seq : id_seqs){
//		std::cerr << id_seq.second << std::endl;
//		std::cerr << trie.search(id_seq.second, 0) << std::endl;
		if(! trie.search(id_seq.second, 0)){
			trie.add(id_seq.second);
			dedup_id_seqs.push_back(id_seq);

//			write_fasta(&std::cerr, dedup_id_seqs);
//			std::cerr << trie.toString() << std::endl;
		}
	}

	std::cerr << string_format("[NOTE] Number of reads (after trie dedup) = %d", dedup_id_seqs.size()) << std::endl;
	return dedup_id_seqs;
}

bool Deduper::checkSeqEqual(std::string seq1, std::string seq2){
	unsigned int len = seq1.length();
	if(seq2.length() != len){
		return false;
	}
	for(unsigned int i=0; i<len; i++){
		if(seq1[i] != seq2[i] && seq1[i] != 'N' && seq2[i] != 'N'){
			return false;
		}
	}
	return true;
}

std::vector<SeqIdAndSeq> Deduper::collapseSeqPairwise(std::vector<SeqIdAndSeq> uniq_id_seqs){
	std::vector<SeqIdAndSeq> dedup_id_seqs;

	std::unordered_map<std::string, void *> uniq_hash;
	ACGTNTrieNode trie;
	for(unsigned int k=0; k<uniq_id_seqs.size(); k++){
		SeqIdAndSeq id_seq = uniq_id_seqs[k];
		bool has_found = false;
		for ( auto it = uniq_hash.begin(); it != uniq_hash.end(); it++ ){
			if(Deduper::checkSeqEqual(id_seq.second, it->first)){
				has_found = true;
				break;
			}
		}
		if(! has_found){
			uniq_hash[id_seq.second] = (void *) NULL;
			dedup_id_seqs.push_back(id_seq);
		}
	}

	std::cerr << string_format("[NOTE] Number of reads (after pairwise dedup) = %d", dedup_id_seqs.size()) << std::endl;
	return dedup_id_seqs;
}


