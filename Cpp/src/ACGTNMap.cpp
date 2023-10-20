/*
 * ACGTNMap.cpp
 *
 *  Created on: Jan 28, 2023
 *      Author: Adam Yongxin Ye @ BCH
 */

#include <vector>
#include <string>

#include "ACGTNMap.h"
#include "YyxUtils.h"

// reference: https://stackoverflow.com/questions/7433448/eclipse-cdt-symbol-null-could-not-be-resolved
#ifndef NULL
#define NULL  ((void *) 0)
#endif

#define ACGTN_SIZE 5

char ACGTNMap::keys_array[ACGTN_SIZE] = {'A', 'C', 'G', 'T', 'N'};

int ACGTNMap::char2idx(char ch){
	if(ch < 'G'){
		if(ch=='A'){
			return 0;
		}else if(ch=='C'){
			return 1;
		}
	}else{
		if(ch=='G'){
			return 2;
		}else if(ch=='T'){
			return 3;
		}else if(ch=='N'){
			return 4;
		}
	}
	return -1;
}

ACGTNMap::ACGTNMap() {
	storage = new void* [ACGTN_SIZE];
	for(int i=0; i<ACGTN_SIZE; i++){
		storage[i] = NULL;
	}
//	storage_size = 0;
}

ACGTNMap::~ACGTNMap() {
	delete [] storage;
}

bool ACGTNMap::containsKey(char key){
	int idx = char2idx(key);
	if(idx >= 0){
		if(storage[idx] != NULL){
			return true;
		}
	}
	return false;
}

void * ACGTNMap::get(char key){
	int idx = char2idx(key);
	if(idx >= 0){
		return storage[idx];
	}else{
		return NULL;
	}
}

void * ACGTNMap::put(char key, void * value){
	int idx = char2idx(key);
	if(idx >= 0){
		void * prevValue = storage[idx];
		storage[idx] = value;
//		if(prevValue == NULL){
//			this->storage_size++;
//		}
		return prevValue;
	}else{
		return NULL;
	}
}

void * ACGTNMap::remove(char key){
	int idx = char2idx(key);
	if(idx >= 0){
		void * prevValue = storage[idx];
		storage[idx] = NULL;
//		if(prevValue != NULL){
//			this->storage_size--;
//		}
		return prevValue;
	}else{
		return NULL;
	}
}

//void ACGTNMap::delete_contents(){
//	for(int i=0; i<ACGTN_SIZE; i++){
//		if(storage[i] != NULL){
//			delete storage[i];  // TODO: deleting 'void*' is undefined
//			storage[i] = NULL;
//		}
//	}
////	this->storage_size = 0;
//}

//int ACGTNMap::size(){
//	return storage_size;
//}

std::vector<char> ACGTNMap::keyVec(){
	std::vector<char> ans;
//	ans.reserve(ACGTN_SIZE);
	for(int i=0; i<ACGTN_SIZE; i++){
		if(storage[i] != NULL){
			ans.push_back(keys_array[i]);
		}
	}
	return ans;
}

std::vector<std::pair<char, void *>> ACGTNMap::entryVec(){
	std::vector<std::pair<char, void *>> ans;
//	ans.reserve(ACGTN_SIZE);  // TODO: test whether this capacity initialization helps ?
	for(int i=0; i<ACGTN_SIZE; i++){
		if(storage[i] != NULL){
			ans.push_back(std::make_pair(keys_array[i], storage[i]));
		}
	}
	return ans;
}

std::string ACGTNMap::toString(){
	std::string ans = "";
	for(int i=0; i<ACGTN_SIZE; i++){
		if(storage[i] != NULL){
			if(ans != ""){
				ans += ", ";
			}
			ans += string_format("%s : %s", keys_array[i], storage[i]);
		}
	}
	return "{" + ans + "}";
}

#undef ACGTN_SIZE
