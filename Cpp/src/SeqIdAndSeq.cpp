/*
 * SeqIdAndSeq.cpp
 *
 *  Created on: Jan 28, 2023
 *      Author: Adam Yongxin Ye @ BCH
 */

#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>

#include "SeqIdAndSeq.h"
#include "YyxUtils.h"

void write_fasta(std::ostream *out, std::vector<SeqIdAndSeq> id_seqs){
	for(unsigned int k=0; k<id_seqs.size(); k++){
		SeqIdAndSeq id_seq = id_seqs[k];
//	for(SeqIdAndSeq id_seq : id_seqs){
		*out << ">" << id_seq.first << std::endl;
		*out << id_seq.second << std::endl;
	}
}

// reference: https://www.techiedelight.com/trim-string-cpp-remove-leading-trailing-spaces/
std::string chomp(const std::string &s)
{
    size_t end = s.find_last_not_of("\n\r");
    return (end == std::string::npos) ? "" : s.substr(0, end + 1);
}

std::vector<SeqIdAndSeq> read_fasta(std::string input_path){
	std::vector<SeqIdAndSeq> id_seqs;
	std::cerr << "[STEP] opening fasta file '" << input_path << "' ..." << std::endl;
	std::string now_name = "";
	std::string now_seq = "";
	// reference: https://stackoverflow.com/questions/7868936/read-file-line-by-line-using-ifstream-in-c
	std::string line;
	std::ifstream infile(input_path);
	if(! infile.good()){
		std::cerr << "Error: cannot open '" << input_path << "' for input" << std::endl;
		return id_seqs;
	}
	while(std::getline(infile, line)){
		line = chomp(line);
		if(line[0] == '>'){
			if(now_name != ""){
				// reference: https://stackoverflow.com/questions/14265581/parse-split-a-string-in-c-using-string-delimiter-standard-c
				now_name = now_name.substr(0, now_name.find(" "));
				id_seqs.push_back(std::make_pair(now_name, now_seq));
			}
			now_name = line.substr(1);
			now_seq = "";
		}else{
			// reference: https://stackoverflow.com/questions/735204/convert-a-string-in-c-to-upper-case
			std::transform(line.begin(), line.end(), line.begin(), ::toupper);
			now_seq += line;
		}
	}
	if(now_name != ""){
		// reference: https://stackoverflow.com/questions/14265581/parse-split-a-string-in-c-using-string-delimiter-standard-c
		now_name = now_name.substr(0, now_name.find(" "));
		id_seqs.push_back(std::make_pair(now_name, now_seq));
	}
	return id_seqs;
}

std::vector<SeqIdAndSeq> read_fastq(std::string input_path, int min_baseQ, int baseQ_coding_shift){
	std::vector<SeqIdAndSeq> id_seqs;
	std::cerr << "[STEP] opening fastq file '" << input_path << "' ..." << std::endl;
	std::string now_name = "";
	std::string now_seq = "";
	// reference: https://stackoverflow.com/questions/7868936/read-file-line-by-line-using-ifstream-in-c
	std::string lines[4];
	unsigned long NR = 1;
	std::ifstream infile(input_path);
	if(! infile.good()){
		std::cerr << "Error: cannot open '" << input_path << "' for input" << std::endl;
		return id_seqs;
	}
	while(std::getline(infile, lines[0]) && std::getline(infile, lines[1])){
		std::getline(infile, lines[2]);
		std::getline(infile, lines[3]);

		lines[0] = chomp(lines[0]);
		lines[1] = chomp(lines[1]);
		lines[3] = chomp(lines[3]);
		if(lines[0][0] == '@'){
			now_name = lines[0].substr(1);
			now_seq = lines[1];

			if(min_baseQ > 0){
				// convert bases with lower baseQ to Ns
				if(lines[1].length() != lines[3].length()){
					std::cerr << "Warning: invalid fastq format: different length of bases and baseQs at Line " << (NR+1) << " and " << (NR+3) << std::endl;
				}
				unsigned int len = lines[1].length();
				if(lines[3].length() < len){
					len = lines[3].length();
				}
				for(unsigned int i=0; i<len; i++){
					if(lines[3][i] + baseQ_coding_shift < min_baseQ){
						now_seq[i] = 'N';
					}
				}
			}

			id_seqs.push_back(std::make_pair(now_name, now_seq));
		}else{
			std::cerr << "Warning: invalid fastq format: first line not start with @ for Line " << NR << std::endl;
		}
		NR += 4;
	}
	return id_seqs;
}

