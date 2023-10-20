/*
 * ACGTNMap.h
 *
 *  Created on: Jan 28, 2023
 *      Author: Adam Yongxin Ye @ BCH
 */

#ifndef ACGTNMAP_H_
#define ACGTNMAP_H_

#include <vector>
#include <string>

class ACGTNMap {
private:
	void ** storage;
//	int storage_size;

public:
	static char keys_array[];
	static int char2idx(char ch);

	ACGTNMap();
	virtual ~ACGTNMap();

	bool containsKey(char key);
	void * get(char key);
	void * put(char key, void * value);
	void * remove(char key);
//	void delete_contents();
//	int size();

	std::vector<char> keyVec();
	std::vector<std::pair<char, void *>> entryVec();
	std::string toString();
};

#endif /* ACGTNMAP_H_ */
