/*
 * ACGTNTrieNode.h
 *
 *  Created on: Jan 28, 2023
 *      Author: Adam Yongxin Ye @ BCH
 */

#ifndef ACGTNTRIENODE_H_
#define ACGTNTRIENODE_H_

#include "ACGTNMap.h"

class ACGTNTrieNode {
public:
	ACGTNMap *child;
	bool end;

	ACGTNTrieNode();
	virtual ~ACGTNTrieNode();

	void add(std::string sequence);
	bool contains(std::string element);
	bool search(std::string sequence, unsigned int i);
	std::string search_with_traceback(std::string sequence, unsigned int i);
	bool exactMatch(std::string sequence, unsigned int i);
//	int pop(std::string sequence, int i);

	std::string toString(int depth = 9999);
};

#endif /* ACGTNTRIENODE_H_ */
