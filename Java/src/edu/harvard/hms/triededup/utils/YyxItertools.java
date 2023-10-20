package edu.harvard.hms.triededup.utils;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

@SuppressWarnings("rawtypes")
public class YyxItertools {
	// ref: https://stackoverflow.com/questions/8710719/generating-an-alphabetic-sequence-in-java
	
	public static Iterable<List> product(List<List> input_lists){
		final List<List> lists = input_lists;
		final int len = lists.size();
		final int[] sizes = new int[len];
		final int[] zero_idxes = new int[len];
		final List init_ans = new ArrayList();
		for(int k=0; k<len; k++){
			sizes[k] = lists.get(k).size();
			init_ans.add(input_lists.get(k).get(0));
		}
		
		return new Iterable<List>(){
			@Override
			public Iterator<List> iterator() {
				return new Iterator<List>(){
					int[] idxes = zero_idxes;
					List next_ans = init_ans;
					
					@Override
					public boolean hasNext() {
						return next_ans != null;
					}

					@Override
					public List next() {
//						System.err.print("[DEBUG] next->current: ");
//						System.err.println(next_ans==null ? "null" : next_ans.toString());
//						System.err.print("[DEBUG] hasNext: ");
//						System.err.println(this.hasNext());
						if(next_ans==null){
							return null;
						}
						List current_ans = next_ans;
						
						int k = len - 1;
						idxes[k]++;
						while(idxes[k] >= sizes[k]){
							idxes[k] = 0;
							k--;
							if(k < 0){
//								idxes[0] = sizes[0];
								next_ans = null; 
//								System.err.print("[DEBUG] new next: ");
//								System.err.println(next_ans==null ? "null" : next_ans.toString());
//								System.err.print("[DEBUG] hasNext: ");
//								System.err.println(this.hasNext());
//								System.err.print("[DEBUG] current: ");
//								System.err.println(current_ans==null ? "null" : current_ans.toString());
								return current_ans;
							}
							idxes[k]++;
						}
						
						next_ans = new ArrayList();
						if(k > 0){
							next_ans.addAll(current_ans.subList(0, k));
						}
						next_ans.add(input_lists.get(k).get(idxes[k]));
						if(k+1 < len){
							next_ans.addAll(init_ans.subList(k+1, len));
						}
						
//						System.err.print("[DEBUG] new next: ");
//						System.err.println(next_ans==null ? "null" : next_ans.toString());
//						System.err.print("[DEBUG] hasNext: ");
//						System.err.println(this.hasNext());
//						System.err.print("[DEBUG] current: ");
//						System.err.println(current_ans==null ? "null" : current_ans.toString());
						return current_ans;
					}
				};
			}
		};
	}
	
	public static Iterable<List> product(List input_list, int repeats){
		final List<List> input_lists = new ArrayList<List>();
		for(int k=0; k<repeats; k++){
			input_lists.add(input_list);
		}
		return product(input_lists);
	}
	
	public static String list2str(List list){
		StringBuilder sb = new StringBuilder();
		for(Object e : list){
			sb.append(e);
		}
		return sb.toString();
	}
	
	public static List<Character> str2charList(String str){
		// ref: https://www.geeksforgeeks.org/convert-a-string-to-a-list-of-characters-in-java/
		List<Character> ans = new ArrayList<Character>();
		for(char ch : str.toCharArray()){
			ans.add(ch);
		}
		return ans;
	}
	
	
	public static void main(String[] args) {
		// only for debug tests
		final List input_list = Arrays.asList('A', 'B', 'C');
//		Iterator<List> it = product(input_list, 3).iterator();
//		while(it.hasNext()){
//			List now_list = it.next();
//			System.out.println(now_list.toString());
//		}
		
		for(final List now_list : product(input_list, 3)){
//			System.out.println(now_list.toString());
//			StringBuilder sb = new StringBuilder();
//			for(Object e : now_list){
//				sb.append(e);
//			}
//			System.out.println(sb.toString());
			System.out.println(list2str(now_list));
		}
	}
}
