/**
 * 
 */
package edu.harvard.hms.triededup.utils;

import java.util.Collection;
import java.util.List;
import java.util.Map;

/**
 * A class like TrieNode, but only for ACGTN
 * 
 * @author Adam Yongxin Ye & Jianqiao Hu @ BCH
 *
 */
public class ACGTNTrieNode {
	static final int keys_size = ACGTNEnum.values().length;

	public ACGTNMap child;
	public boolean end;
	
	public ACGTNTrieNode() {
		super();
		this.child = new ACGTNMap();
		this.end = false;
	}
	public ACGTNTrieNode(Collection<String> iterable) {
		super();
		this.child = new ACGTNMap();
		this.end = false;
		for(String element : iterable){
			this.add(element);
		}
	}
	
	public void add(String sequence) {
		ACGTNTrieNode node = this;
		for(char base : sequence.toCharArray()){
			if(! node.child.containsKey(base)){
				node.child.put(base, new ACGTNTrieNode());
			}
			node = (ACGTNTrieNode)node.child.get(base);
		}
		node.end = true;
	}

	public boolean contains(String element){
		ACGTNTrieNode node = this;
		for(char k : element.toCharArray()){
			if(! node.child.containsKey(k)){
				return false;
			}
			node =  (ACGTNTrieNode)node.child.get(k);
		}
		return node.end;
	}
	
	public boolean search(String sequence, int i){
		if(i == sequence.length()){
			return this.end;
		}else{
			char query = sequence.charAt(i);
			List<Map.Entry<Character, Object>> entrylist = this.child.entryList();
			for(Map.Entry<Character, Object> entry : entrylist){
				char base = entry.getKey().charValue();
				if(query == base || query == 'N' || base == 'N'){
					if(((ACGTNTrieNode)(entry.getValue())).search(sequence, i+1)){
						return true;
					}
				}
			}
		}
		return false;
	}
	
	public String search_with_traceback(String sequence, int i){
		if(i == sequence.length()){
			if(this.end){
				return "";
			}else{
				return "NULL";
			}
		}else{
			char query = sequence.charAt(i);
			List<Map.Entry<Character, Object>> entrylist = this.child.entryList();
			for(Map.Entry<Character, Object> entry : entrylist){
				char base = entry.getKey().charValue();
				if(query == base || query == 'N' || base == 'N'){
					String inner_result = ((ACGTNTrieNode)(entry.getValue())).search_with_traceback(sequence, i+1);
					if(!inner_result.equals("NULL")){
						return base + inner_result;
					}
				}
			}
		}
		return "NULL";
	}
	
	public boolean exactMatch(String sequence, int i){
		if(i == sequence.length()){
			return this.end;
		}else{
			char base = sequence.charAt(i);
			if(this.child.containsKey(base)){
				return ((ACGTNTrieNode)(this.child.get(base))).exactMatch(sequence,  i+1);
			}
		}
		return false;
	}
	
	public int pop(String sequence, int i){
		if(i == sequence.length()){
			boolean ans = this.end;
			if(ans){
				this.end = false;
				return 1;
			}
		}else{
			char base = sequence.charAt(i);
			if(this.child.containsKey(base)){
				int leaf_ans = ((ACGTNTrieNode)(this.child.get(base))).pop(sequence, i+1);
				if(leaf_ans == 1){
					if(this.child.size() == 1){
						this.child.remove(base);
					}else{
						leaf_ans = 2;
					}
				}
				return leaf_ans;
			}
//			char query = sequence.charAt(i);
//			List<Map.Entry<Character, Object>> entrylist = this.child.entryList();
//			for(Map.Entry<Character, Object> entry : entrylist){
//				char base = entry.getKey().charValue();
//				if(query == base){
//					int leaf_ans = ((ACGTNTrieNode)(entry.getValue())).pop(sequence, i+1);
//					if(leaf_ans == 1){
//						if(entrylist.size() == 1){
//							this.child.remove(base);
//						}else{
//							leaf_ans = 2;
//						}
//					}
//					return leaf_ans;
//				}
//			}
		}
		return 0;
	}
}

