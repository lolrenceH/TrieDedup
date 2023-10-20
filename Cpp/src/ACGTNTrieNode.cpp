/*
 * ACGTNTrieNode.cpp
 *
 *  Created on: Jan 28, 2023
 *      Author: Adam Yongxin Ye @ BCH
 */

//#include <iostream>

#include "ACGTNTrieNode.h"
#include "ACGTNMap.h"

#define ACGTN_SIZE 5

ACGTNTrieNode::ACGTNTrieNode() {
	child = new ACGTNMap;
	end = false;
}

ACGTNTrieNode::~ACGTNTrieNode() {
//	child->delete_contents();
//	for(char base : {'A', 'C', 'G', 'T', 'N'}){
	for(int i=0; i<ACGTN_SIZE; i++){
		char base = ACGTNMap::keys_array[i];
		void *ptr = child->get(base);
		if(ptr != NULL){
			delete (ACGTNTrieNode *)ptr;  // TODO: deleting 'void*' is undefined
		}
	}
	delete child;
}

void ACGTNTrieNode::add(std::string sequence){
	ACGTNTrieNode *node = this;
	for(unsigned int i=0; i<sequence.length(); i++){
		char base = sequence[i];
//	for(char base : sequence){
		if(! node->child->containsKey(base)){
			node->child->put(base, new ACGTNTrieNode);
		}
		node = (ACGTNTrieNode *)node->child->get(base);
	}
	node->end = true;
}

bool ACGTNTrieNode::contains(std::string sequence){
	ACGTNTrieNode *node = this;
	for(unsigned int i=0; i<sequence.length(); i++){
		char base = sequence[i];
//	for(char base : sequence){
		if(! node->child->containsKey(base)){
			return false;
		}
		node = (ACGTNTrieNode *)node->child->get(base);
	}
	return node->end;
}

bool ACGTNTrieNode::search(std::string sequence, unsigned int i){
	if(i == sequence.length()){
		return this->end;
	}else{
		char query = sequence[i];
		std::vector<std::pair<char, void *>> entry_vec = this->child->entryVec();
		for(unsigned int k=0; k<entry_vec.size(); k++){
			std::pair<char, void *> entry = entry_vec[k];
//		for(std::pair<char, void *> entry : entry_vec){
			char base = entry.first;
//			std::cerr << "query=" << query << " vs base=" << base << std::endl;
			if(query==base || query=='N' || base=='N'){
				if(((ACGTNTrieNode *)entry.second)->search(sequence, i+1)){
					return true;
				}
			}
		}
	}
	return false;
}

std::string ACGTNTrieNode::search_with_traceback(std::string sequence, unsigned int i){
	if(i == sequence.length()){
		if(this->end){
			return "";
		}else{
			return "NULL";
		}
	}else{
		char query = sequence[i];
		std::vector<std::pair<char, void *>> entry_vec = this->child->entryVec();
		for(unsigned int k=0; k<entry_vec.size(); k++){
			std::pair<char, void *> entry = entry_vec[k];
//		for(std::pair<char, void *> entry : entry_vec){
			char base = entry.first;
//			std::cerr << "query=" << query << " vs base=" << base << std::endl;
			if(query==base || query=='N' || base=='N'){
				std::string inner_result = ((ACGTNTrieNode *)entry.second)->search_with_traceback(sequence, i+1);
				if(inner_result != "NULL"){
					return base + inner_result;
				}
			}
		}
	}
	return "NULL";
}

bool ACGTNTrieNode::exactMatch(std::string sequence, unsigned int i){
	if(i == sequence.length()){
		return this->end;
	}else{
		char base = sequence[i];
		if(this->child->containsKey(base)){
			return ((ACGTNTrieNode *)this->child->get(base))->search(sequence, i+1);
		}
	}
	return false;
}

//int ACGTNTrieNode::pop(std::string sequence, int i){
//	if(i == sequence.length()){
//		if(this->end){
//			this->end = false;
//			return 1;
//		}
//	}else{
//		char base = sequence[i];
//		if(this->child->containsKey(base)){
//			int leaf_ans =((ACGTNTrieNode *)this->child->get(base))->pop(sequence, i+1);
//			if(leaf_ans == 1){
//				if(this->child->size() == 1){
//					this->child->remove(base);
//				}else{
//					leaf_ans = 2;
//				}
//			}
//		}
//	}
//	return false;
//}

std::string ACGTNTrieNode::toString(int depth){
	std::string ans = "{";
	if(end){
		ans += "$";
	}
	for(int i=0; i<ACGTN_SIZE; i++){
		char base = ACGTNMap::keys_array[i];
		void *ptr = child->get(base);
		if(ptr != NULL){
			if(ans != "{"){
				ans += ",";
			}
			ans += base;
			if(depth > 0){
				ans += ":" + ((ACGTNTrieNode *)ptr)->toString(depth-1);
			}
		}
	}
	ans += "}";
	return ans;
}

#undef ACGTN_SIZE
