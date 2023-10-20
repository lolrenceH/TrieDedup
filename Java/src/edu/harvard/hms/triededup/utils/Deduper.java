package edu.harvard.hms.triededup.utils;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

class CountN implements Comparator<SeqIdAndSeq>{
	public static int countN(SeqIdAndSeq id_seq){
		int count = 0;
		char[] chs = id_seq.sequence.toCharArray();
		for(int i=0; i<chs.length; i++){
			if(chs[i] == 'N'){
				count++;
			}
		}
		return count;
	}
	
	@Override
	public int compare(SeqIdAndSeq o1, SeqIdAndSeq o2) {
		return CountN.countN(o1) - CountN.countN(o2);
	}
}

/**
 * A class wrapping uniq_and_sort and collapseSeq (trie or pairwise)
 * 
 * @author Adam Yongxin Ye & Jianqiao Hu @ BCH
 *
 */
public class Deduper {
	public static List<SeqIdAndSeq> uniq_and_sort(List<SeqIdAndSeq> id_seqs, boolean is_input_sorted, int max_missing){
		System.err.println(String.format("[NOTE] Number of reads (raw) = %d", id_seqs.size()));
		YyxTimer tm = new YyxTimer();
		Set<String> uniq_seqs_hash = new HashSet<String>();
		List<SeqIdAndSeq> uniq_id_seqs = new ArrayList<SeqIdAndSeq>();
		int lastCountN = -1;
		int currentCountN;
		System.err.print(String.format("[STEP] uniqueing and filtering out sequences with too many Ns ..."));
		for(SeqIdAndSeq id_seq : id_seqs){
			if(! uniq_seqs_hash.contains(id_seq.sequence)){
				uniq_seqs_hash.add(id_seq.sequence);
				currentCountN = CountN.countN(id_seq);
				if(is_input_sorted){
					if(currentCountN < lastCountN){
						// violate the assumption of input already sorted
						System.err.print("Warning: some later sequence has fewer Ns than previous sequence, which violates the assumption of sorted input, so I will set is_input_sorted = false instead");
						is_input_sorted = false;
					}else{
						lastCountN = currentCountN;
					}
				}
				if(currentCountN <= max_missing){
					uniq_id_seqs.add(id_seq);
				}else if(is_input_sorted){
					break;
				}
			}
		}
		System.err.println(String.format(" \t%s", tm.elapsedTimeString()));
		System.err.println(String.format("[NOTE] Number of reads (filtered out too many Ns) = %d", uniq_id_seqs.size()));
		
		if(! is_input_sorted){
			System.err.print(String.format("[STEP] sorting ..."));
			tm.resetTime();
			uniq_id_seqs.sort(new CountN());
			System.err.println(String.format(" \t%s", tm.elapsedTimeString()));
		}
		return uniq_id_seqs;
	}
	
	
	public static List<SeqIdAndSeq> collapseSeqTrie(List<SeqIdAndSeq> uniq_id_seqs){
//		List<SeqIdAndSeq> uniq_id_seqs = Deduper.uniq_and_sort(id_seqs, is_input_sorted, max_missing);
		List<SeqIdAndSeq> dedup_id_seqs = new ArrayList<SeqIdAndSeq>();

		ACGTNTrieNode trie = new ACGTNTrieNode();
		for(SeqIdAndSeq id_seq : uniq_id_seqs){
//			// for debug
//			if(id_seq.seqId.equals("200")){
//				System.err.println(id_seq.sequence);
//				System.err.println(trie.search(id_seq.sequence, 0));
//				System.err.println(trie.search_with_traceback(id_seq.sequence, 0));
//			}
			if(! trie.search(id_seq.sequence, 0)){   // not found
				trie.add(id_seq.sequence);
				dedup_id_seqs.add(id_seq);
			}
		}
		
		System.err.println(String.format("[NOTE] Number of reads (after trie dedup) = %d", dedup_id_seqs.size()));
		return dedup_id_seqs;
	}
	
	
	public static boolean checkSeqEqual(String seq1, String seq2){
		int len = seq1.length();
		if(seq2.length() != len){
			return false;
		}
		char[] chs1 = seq1.toCharArray();
		char[] chs2 = seq2.toCharArray();
		for(int i=0; i<len; i++){
			if(chs1[i] != chs2[i] && chs1[i] != 'N' && chs2[i] != 'N'){
				return false;
			}
		}
		return true;
	}
	
	public static List<SeqIdAndSeq> collapseSeqPairwise(List<SeqIdAndSeq> uniq_id_seqs){
//		List<SeqIdAndSeq> uniq_id_seqs = Deduper.uniq_and_sort(id_seqs, is_input_sorted, max_missing);
		List<SeqIdAndSeq> dedup_id_seqs = new ArrayList<SeqIdAndSeq>();
		
		Set<String> uniq_hash = new HashSet<String>();
		for(SeqIdAndSeq id_seq : uniq_id_seqs){
			boolean has_found = false;
			for(String sbjt : uniq_hash){
				if(Deduper.checkSeqEqual(id_seq.sequence, sbjt)){
					has_found = true;
					break;
				}
			}
			if(! has_found){   // not found
				uniq_hash.add(id_seq.sequence);
				dedup_id_seqs.add(id_seq);
			}
		}
		
		System.err.println(String.format("[NOTE] Number of reads (after pairwise dedup) = %d", uniq_hash.size()));
		return dedup_id_seqs;
	}
}
