/*
 * Main.cpp
 *
 *  Created on: Jan 30, 2023
 *      Author: Adam Yongxin Ye @ BCH
 */


// reference: https://linux.die.net/man/3/getopt , https://cplusplus.com/articles/DEN36Up4/
//#include <stdio.h>     /* for printf */
#include <cstdlib>    /* for strtol & exit */
#include <getopt.h>
#include <iostream>
#include <vector>
#include <fstream>
#include <unordered_map>

#ifdef WINDOWS
#include <direct.h>
#define GetCurrentDir _getcwd
#else
#include <unistd.h>
#define GetCurrentDir getcwd
#endif

#include "Timer.h"
#include "YyxUtils.h"
#include "SeqIdAndSeq.h"
#include "Deduper.h"
#include "ACGTNTrieNode.h"


static std::string version = "\n"
"Version: 0.1.1 (2024-03-12)\n"
"Author: Adam Yongxin Ye & Jianqiao Hu @ BCH\n";

static void show_usage(std::string program_name)
{
	std::cout << "Usage: " << program_name << std::endl;
	std::cout << "\t [options] <command> <input>" << std::endl;
	std::cout << "Options:" << std::endl;
	std::cout << "    -h|--help \t\t\tshow this command-line help page" << std::endl;
	std::cout << "    -o|--output <file> \t\tset output file path (default: STDOUT)" << std::endl;
	std::cout << "    -s|--sorted \t\tinput already uniq and sorted (default: false)" << std::endl;
	std::cout << "    -m|--max-missing <int> \tmax number of Ns allowed for each read (default: 9999)" << std::endl;
	std::cout << "    -q|--min-baseQ <int> \tbases with lower baseQ will be converted to N (default: 0)" << std::endl;
	std::cout << "    -t|--baseQ-shift <int> \tbaseQ value shifted from char (default: 33)" << std::endl;
	std::cout << "    -f|--output-format <str> \toutput format [readID, sequence, fasta, dup2uniq, uniq2dup] (default: fasta)" << std::endl;
	std::cout << "Supported <command>:" << std::endl;
	std::cout << "    sortuniq \tjust uniq by sequence and sort by N, and output fasta" << std::endl;
	std::cout << "    trie \tdeduplicate using trie algorithm" << std::endl;
	std::cout << "    pairwise \tdeduplicate using pairwise algorithm" << std::endl;
	std::cout << "Supported <input> format:" << std::endl;
	std::cout << "    (automatically determined by <input>'s file extension)" << std::endl;
	std::cout << "\t.fasta, .fa, .fastq, .fq" << std::endl;
	std::cout << "Output:  STDOUT  or  -o|--output <file>" << std::endl;
	std::cout << "\tformat specified in -f|--output-format option" << std::endl;
	std::cout << "    If set to dup2uniq, I will output 4-column tsv format: 1st-2nd columns are original readID and sequences, 3rd-4th columns are the mapped deduplicated readID and sequences." << std::endl;
	std::cout << "    If set to uniq2dup, I will output to STDOUT 5-column tsv format: 1st-2nd columns are deduplicated readID and sequences, 3rd column is frequency, 4th column is original readIDs concatenated by ',', 5th column is orignal sequences concatenated by ','." << std::endl;
	std::cout << version << std::endl;
}

struct my_args{
	bool should_help;
	std::string output_filename;
	bool is_input_sorted;
	unsigned int max_missing;
	unsigned int min_baseQ;
	int baseQ_shift;
	std::string command_choose;
	std::string input_filename;
	std::string output_format;
};

struct my_args parse_cmd_args(int argc, char **argv){
	Timer tm;
	std::cerr << "[STEP] parsing command-line arguments ...";

	struct my_args args;
	args.should_help = false;
	args.output_filename = "STDOUT";
	args.is_input_sorted = false;
	args.max_missing = 9999;
	args.min_baseQ = 0;
	args.baseQ_shift = 33;
	args.command_choose = "";
	args.input_filename = "";
	args.output_format = "fasta";

	// reference: https://linux.die.net/man/3/getopt , https://cplusplus.com/articles/DEN36Up4/
	static struct option long_options[] = {
		// const char *name, int has_arg, int *flag, int val
		{"help", no_argument, 0, 0},
		{"output", required_argument, 0, 0},
		{"sorted", no_argument, 0, 0},
		{"max-missing", required_argument, 0, 0},
		{"min-baseQ", required_argument, 0, 0},
		{"baseQ-shift", required_argument, 0, 0},
		{"output-format", required_argument, 0, 0},
		{0, 0, 0, 0}
	};

	int c;
	while(true){
//		int this_option_optind = optind ? optind : 1;
		int option_index = 0;
		c = getopt_long(argc, argv, "ho:sm:q:t:f:", long_options, &option_index);
		if(c == -1){
			break;
		}else if(c == 0){
//			printf("option %s", long_options[option_index].name);
//			if(optarg){
//				printf(" with arg %s", optarg);
//			}
			std::string opt_name(long_options[option_index].name);
			if(opt_name == "help"){
				args.should_help = true;
			}else if(opt_name == "output"){
				args.output_filename = optarg;
			}else if(opt_name == "sorted"){
				args.is_input_sorted = true;
			}else if(opt_name == "max-missing"){
				args.max_missing = strtol(optarg, NULL, 10);
			}else if(opt_name == "min-baseQ"){
				args.min_baseQ = strtol(optarg, NULL, 10);
			}else if(opt_name == "baseQ-shift"){
				args.baseQ_shift = strtol(optarg, NULL, 10);
			}else if(opt_name == "output-format"){
				args.output_format = optarg;
			}else{
				std::cerr << "Error: cannot recognize long option " << opt_name << std::endl;
			}
		}else if(c == 'h'){
			args.should_help = true;
		}else if(c == 'o'){
			args.output_filename = optarg;
		}else if(c == 's'){
			args.is_input_sorted = true;
		}else if(c == 'm'){
			args.max_missing = strtol(optarg, NULL, 10);
		}else if(c == 'q'){
			args.min_baseQ = strtol(optarg, NULL, 10);
		}else if(c == 't'){
			args.baseQ_shift = strtol(optarg, NULL, 10);
		}else if(c == 'f'){
			args.output_format = optarg;
		}
	}

	if (optind < argc - 1) {
		args.command_choose = argv[optind++];
		args.input_filename = argv[optind++];
	}

	std::cerr << " \t" << tm.format_elapsed_time() << std::endl;
	return args;
}

std::string get_current_dir() {
	char buff[FILENAME_MAX]; //create string buffer to hold path
	GetCurrentDir( buff, FILENAME_MAX );
	std::string current_working_dir(buff);
	return current_working_dir;
}

std::string get_file_extension(std::string filename){
	// reference: https://stackoverflow.com/questions/51949/how-to-get-file-extension-from-string-in-c
	return filename.substr(filename.find_last_of(".") + 1);
}

int main(int argc, char **argv){
//	ACGTNTrieNode trie;
//	std::cerr << trie.toString() << std::endl;
//	trie.add("ACGTN");
//	std::cerr << trie.toString() << std::endl;
//	trie.add("GTACN");
//	std::cerr << trie.toString() << std::endl;
//	trie.add("ACTGN");
//	std::cerr << trie.toString() << std::endl;
//	std::cerr.flush();
//	exit(0);

	Timer all_tm;
	struct my_args args = parse_cmd_args(argc, argv);
	if(args.should_help){
		show_usage(argv[0]);
		exit(-1);
	}
	if(args.command_choose=="" || args.input_filename==""){
		std::cerr << "\nError: not enough command-line arguments, need <command> and <input>" << std::endl;
		show_usage(argv[0]);
		exit(-1);
	}
	std::cerr << "  Current working directory = " << get_current_dir() << std::endl;
	std::cerr << "[ARG] command_choose = " << args.command_choose << std::endl;
	std::cerr << "[ARG] input_filename = " << args.input_filename << std::endl;
	std::cerr << "[OPT] sorted = " << args.is_input_sorted << std::endl;
	std::cerr << "[OPT] max_missing = " << args.max_missing << std::endl;
	std::cerr << "[OPT] baseQ_shift = " << args.baseQ_shift << std::endl;
	std::cerr << "[OPT] min_baseQ = " << args.min_baseQ << std::endl;
	std::cerr << "[OPT] output_format = " << args.output_format << std::endl;

	if(args.command_choose != "trie" && args.command_choose != "pairwise" && args.command_choose != "sortuniq"){
		std::cerr << "Error: unknown command = " << args.command_choose << std::endl;
		show_usage(argv[0]);
		exit(-1);
	}
	int *traceback_mapping_vec = NULL;
	std::unordered_map<std::string, int> uniq_seqs_hash;
	std::unordered_map<int, std::vector<int>> uniqIdx2idxes;
	if(args.output_format != "fasta" && args.output_format != "readID" && args.output_format != "sequence" && args.output_format != "dup2uniq" && args.output_format != "uniq2dup"){
		std::cerr << "Error: unknown output_format = " << args.output_format << std::endl;
		show_usage(argv[0]);
		exit(-1);
	}

	std::vector<SeqIdAndSeq> parsed_id_seqs;
	std::string input_file_extension = get_file_extension(args.input_filename);
	Timer tm;
	if(input_file_extension=="fa" || input_file_extension=="fasta"){
		std::cerr << "[STEP] reading sequences in fasta ..." << std::endl;
		parsed_id_seqs = read_fasta(args.input_filename);
	}else if(input_file_extension=="fq" || input_file_extension=="fastq"){
		std::cerr << "[STEP] reading sequences in fastq ..." << std::endl;
		parsed_id_seqs = read_fastq(args.input_filename, args.min_baseQ, -args.baseQ_shift);
	}else{
		std::cerr << "Error: cannot parse input file with extension '" << input_file_extension << "'" << std::endl;
		exit(-2);
	}
	if(parsed_id_seqs.size() <= 0){
		std::cerr << "Error: no sequence is parsed from input file" << std::endl;
		exit(-3);
	}
	std::cerr << "[STEP-TIME] reading " << parsed_id_seqs.size() << " sequences done. \t" << tm.format_elapsed_time() << std::endl;
//	write_fasta(&std::cerr, parsed_id_seqs);

	if(args.output_format == "dup2uniq" || args.output_format == "uniq2dup"){
		traceback_mapping_vec = new int[parsed_id_seqs.size()];
	}

//	std::cerr << "[DEBUG1] traceback_mapping_vec = ";
//	for(unsigned int k=0; k<parsed_id_seqs.size(); k++){
//		if(k>0){
//			std::cerr << ",";
//		}
//		std::cerr << traceback_mapping_vec[k];
//	}
//	std::cerr << std::endl;
//	std::cerr << "[DEBUG1] uniq_seqs_hash = {";
//	for ( auto it = uniq_seqs_hash.begin(); it != uniq_seqs_hash.end(); it++ ){
//		std::cerr << it->first << ":" << it->second << ",";
//	}
//	std::cerr << "}" << std::endl;
//	std::cerr << "[DEBUG1] uniqIdx2idxes = {";
//	for ( auto it = uniqIdx2idxes.begin(); it != uniqIdx2idxes.end(); it++ ){
//		std::cerr << it->first << ":";
//		for ( auto it2 = it->second.begin(); it2 != it->second.end(); it2++ ){
//			std::cerr << (*it2) << ",";
//		}
//		std::cerr << ";";
//	}
//	std::cerr << "}" << std::endl;

	std::vector<SeqIdAndSeq> uniq_id_seqs = parsed_id_seqs;
//	write_fasta(&std::cerr, uniq_id_seqs);
	tm.reset();
	std::cerr << "[STEP] uniq and sort by N ..." << std::endl;
	uniq_id_seqs = Deduper::uniq_and_sort(parsed_id_seqs, args.is_input_sorted, args.max_missing, traceback_mapping_vec, uniq_seqs_hash, uniqIdx2idxes);
	std::cerr << "[STEP-TIME] uniq and sort done. \t" << tm.format_elapsed_time() << std::endl;
	std::cerr << string_format("[NOTE] Uniq and sort resulted in %d unique reads.", uniq_id_seqs.size()) << std::endl;
//	write_fasta(&std::cerr, uniq_id_seqs);

//	std::cerr << "[DEBUG2] traceback_mapping_vec = ";
//	for(unsigned int k=0; k<parsed_id_seqs.size(); k++){
//		if(k>0){
//			std::cerr << ",";
//		}
//		std::cerr << traceback_mapping_vec[k];
//	}
//	std::cerr << std::endl;
//	std::cerr << "[DEBUG2] uniq_seqs_hash = {";
//	for ( auto it = uniq_seqs_hash.begin(); it != uniq_seqs_hash.end(); it++ ){
//		std::cerr << it->first << ":" << it->second << ",";
//	}
//	std::cerr << "}" << std::endl;
//	std::cerr << "[DEBUG2] uniqIdx2idxes = {";
//	for ( auto it = uniqIdx2idxes.begin(); it != uniqIdx2idxes.end(); it++ ){
//		std::cerr << it->first << ":";
//		for ( auto it2 = it->second.begin(); it2 != it->second.end(); it2++ ){
//			std::cerr << (*it2) << ",";
//		}
//		std::cerr << ";";
//	}
//	std::cerr << "}" << std::endl;

	if(args.command_choose != "sortuniq"){   // need deduplication
		//deduplication
		tm.reset();
		if(args.command_choose == "trie"){
			std::cerr << "[STEP] deduplicating by trie ..." << std::endl;
			uniq_id_seqs = Deduper::collapseSeqTrie(uniq_id_seqs, traceback_mapping_vec, uniq_seqs_hash, uniqIdx2idxes);
		}else if(args.command_choose == "pairwise"){
			std::cerr << "[STEP] deduplicating by pairwise ..." << std::endl;
			uniq_id_seqs = Deduper::collapseSeqPairwise(uniq_id_seqs, traceback_mapping_vec, uniq_seqs_hash, uniqIdx2idxes);
		}
		std::cerr << "[STEP-TIME] deduplication done. \t" << tm.format_elapsed_time() << std::endl;
		std::cerr << string_format("[NOTE] Deduplicating resulted in %d unique reads.", uniq_id_seqs.size()) << std::endl;
	}

//	std::cerr << "[DEBUG3] traceback_mapping_vec = ";
//	for(unsigned int k=0; k<parsed_id_seqs.size(); k++){
//		if(k>0){
//			std::cerr << ",";
//		}
//		std::cerr << traceback_mapping_vec[k];
//	}
//	std::cerr << std::endl;

	// output
	tm.reset();
	std::cerr << "[STEP] output to " << args.output_filename << " ..." << std::endl;
	// reference: https://stdcxx.apache.org/doc/stdlibug/34-2.html
	std::ostream *out;
	std::ofstream outfile;
	if(args.output_filename == "STDOUT"){
		out = &std::cout;
	}else{
		outfile.open(args.output_filename);
		out = &outfile;
	}
	if(args.output_format == "fasta"){
		write_fasta(out, uniq_id_seqs);
	}else if(args.output_format == "readID"){
		for(unsigned int k=0; k<uniq_id_seqs.size(); k++){
			SeqIdAndSeq id_seq = uniq_id_seqs[k];
			*out << id_seq.first << std::endl;
		}
	}else if(args.output_format == "sequence"){
		for(unsigned int k=0; k<uniq_id_seqs.size(); k++){
			SeqIdAndSeq id_seq = uniq_id_seqs[k];
			*out << id_seq.second << std::endl;
		}
	}else if(args.output_format == "dup2uniq"){
		for(unsigned int k=0; k<parsed_id_seqs.size(); k++){
			int uniqIdx = traceback_mapping_vec[k];
			SeqIdAndSeq orig_id_seq = parsed_id_seqs[k];
			SeqIdAndSeq uniq_id_seq = parsed_id_seqs[uniqIdx];
			*out << orig_id_seq.first << "\t" << orig_id_seq.second << "\t" << uniq_id_seq.first << "\t" << uniq_id_seq.second << std::endl;
		}
	}else if(args.output_format == "uniq2dup"){
		for(unsigned int k=0; k<uniq_id_seqs.size(); k++){
			SeqIdAndSeq uniq_id_seq = uniq_id_seqs[k];
			int uniqIdx = uniq_seqs_hash[uniq_id_seq.second];
			std::vector<int> idxes = uniqIdx2idxes[uniqIdx];
			*out << uniq_id_seq.first << "\t" << uniq_id_seq.second << "\t" << idxes.size() << "\t";
			for(unsigned int i=0; i<idxes.size(); i++){
				int now_idx = idxes[i];
				SeqIdAndSeq orig_id_seq = parsed_id_seqs[now_idx];
				if(i>0){
					*out << ",";
				}
				*out << orig_id_seq.first;
			}
			*out << "\t";
			for(unsigned int i=0; i<idxes.size(); i++){
				int now_idx = idxes[i];
				SeqIdAndSeq orig_id_seq = parsed_id_seqs[now_idx];
				if(i>0){
					*out << ",";
				}
				*out << orig_id_seq.second;
			}
			*out << std::endl;
		}
	}
	out->flush();
	if(args.output_filename != "STDOUT"){
		outfile.close();
	}

	std::cerr << "[STEP-TIME] output done. \t" << tm.format_elapsed_time() << std::endl;
	if(traceback_mapping_vec != NULL){
		delete traceback_mapping_vec;
	}
	std::cerr << "[ALL-TIME] all done. \t" << all_tm.format_elapsed_time() << std::endl;

	exit(0);
}
