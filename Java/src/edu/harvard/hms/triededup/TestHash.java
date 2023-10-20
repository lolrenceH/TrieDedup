package edu.harvard.hms.triededup;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;

import edu.harvard.hms.triededup.utils.YyxItertools;
import edu.harvard.hms.triededup.utils.YyxTimer;

public class TestHash {
	
	public static void main(String[] args) {
		// Usage: java -jar this.jar <HashSet|HashMap> <query_len> [letter_num (default:26)]
		String query_data_structure = args[0];
		int query_len = Integer.parseInt(args[1]);
		int letter_num = 26;
		if(args.length > 2){
			letter_num = Integer.parseInt(args[2]);
		}
		System.err.println("[CMD-ARG] query_data_structure = '" + query_data_structure + "'");
		System.err.println("[CMD-ARG] query_len = '" + String.valueOf(query_len) + "'");
		System.err.println("[CMD-ARG] letter_num = '" + String.valueOf(letter_num) + "'");
		
		List<Character> query_letters = new ArrayList<Character>();
		for(int ch=65; ch<65+letter_num; ch++){
			query_letters.add((char)ch);
		}
		
		
		YyxTimer tm = new YyxTimer();
		
		if(query_data_structure.equals("HashSet")){
			HashSet<String> my_dict = new HashSet<String>();
			for(List now_list : YyxItertools.product(query_letters, query_len)){
				my_dict.add(YyxItertools.list2str(now_list));
			}
		}else if(query_data_structure.equals("HashMap")){
			boolean[] oneTrue = new boolean[]{true};
			HashMap<String, boolean[]> my_dict = new HashMap<String, boolean[]>();
			for(List now_list : YyxItertools.product(query_letters, query_len)){
				my_dict.put(YyxItertools.list2str(now_list), oneTrue);
			}
		}else{
			System.err.println("Error: unrecognized query_data_structure = '" + query_data_structure + "'");
		}
		
		System.err.println(String.format("[JAVA-TIME] hash done. \t%s", tm.elapsedTimeString()));
	}

}
