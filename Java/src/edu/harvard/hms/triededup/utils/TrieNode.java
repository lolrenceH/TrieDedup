/**
 * 
 */
package edu.harvard.hms.triededup.utils;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Custom class of the trie (prefix tree) node: TrieNode
 * the recursive algorithm for checking if a query sequence exists in the input trie
 * 
 * @author Adam Yongxin Ye & Jianqiao Hu @ BCH
 *
 */
@SuppressWarnings("rawtypes")
public class TrieNode {
	public List<Character> keys;
	public Map<Character, TrieNode> child;
	public boolean end;
	
	public TrieNode() {
		super();
		this.keys = new ArrayList();
		this.child = new HashMap();
		this.end = false;
	}
	public TrieNode(Collection<String> iterable) {
		super();
		this.keys = new ArrayList();
		this.child = new HashMap();
		this.end = false;
		for(String element : iterable){
			this.add(element);
		}
	}
	
	public void add(String sequence) {
		TrieNode node = this;
		for(char base : sequence.toCharArray()){
			if(! node.child.containsKey(base)){
				int len = node.keys.size();
				if(len > 0 && node.keys.get(len-1) == 'N'){
					node.keys.add(len-1, base);
				}else{
					node.keys.add(base);
				}
				node.child.put(base, new TrieNode());
			}
			node = node.child.get(base);
		}
		node.end = true;
	}

	public boolean contains(String element){
		TrieNode node = this;
		for(char k : element.toCharArray()){
			if(!node.keys.contains(k)){
				return false;
			}
			node = node.child.get(k);
		}
		return node.end;
	}
	
	public boolean search(String sequence, int i){
		if(i == sequence.length()){
			return this.end;
		}else{
			char query = sequence.charAt(i);
			for(char base : this.keys){
				if(query == base || query == 'N' || base == 'N'){
					if(this.child.get(base).search(sequence, i+1)){
						return true;
					}
				}
			}
		}
		return false;
	}
	
	public boolean exactMatch(String sequence, int i){
		if(i == sequence.length()){
			return this.end;
		}else{
			char base = sequence.charAt(i);
			if(this.child.containsKey(base)){
				return this.child.get(base).exactMatch(sequence,  i+1);
			}
		}
		return false;
	}
}
