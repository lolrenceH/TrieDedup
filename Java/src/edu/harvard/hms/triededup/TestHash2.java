package edu.harvard.hms.triededup;

import java.util.HashMap;
import java.util.HashSet;

import edu.harvard.hms.triededup.utils.YyxTimer;

public class TestHash2 {
	
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
		
		char query_letters[] = new char[letter_num];
		for(char ch=65; ch<65+letter_num; ch++){
			query_letters[ch-65] = ch;
		}
		
		YyxTimer tm = new YyxTimer();
		
		int idxes[] = new int[query_len];
		char key[] = new char[query_len];
		int k;
		for(k=0; k<query_len; k++){
			idxes[k] = 0;
			key[k] = query_letters[0];
		}
		String key_str;
		
		if(query_data_structure.equals("HashSet")){
			HashSet<String> my_dict = new HashSet<String>();
			
			boolean has_next = true;
			while(has_next){
				key_str = String.valueOf(key);
				my_dict.add(key_str);

				k = query_len - 1;
				idxes[k]++;
				while(idxes[k] >= letter_num){
					idxes[k] = 0;
					key[k] = query_letters[0];
					k--;
					if(k < 0){
						has_next = false;
						break;
					}
					idxes[k]++;
				}
				if(k >= 0){
					key[k] = query_letters[idxes[k]];
				}
			}
			
		}else if(query_data_structure.equals("HashMap")){
			boolean[] oneTrue = new boolean[]{true};
			HashMap<String, boolean[]> my_dict = new HashMap<String, boolean[]>();

			boolean has_next = true;
			while(has_next){
				key_str = String.valueOf(key);
				my_dict.put(key_str, oneTrue);

				k = query_len - 1;
				idxes[k]++;
				while(idxes[k] >= letter_num){
					idxes[k] = 0;
					key[k] = query_letters[0];
					k--;
					if(k < 0){
						has_next = false;
						break;
					}
					idxes[k]++;
				}
				if(k >= 0){
					key[k] = query_letters[idxes[k]];
				}
			}
		}else{
			System.err.println("Error: unrecognized query_data_structure = '" + query_data_structure + "'");
		}
		
		System.err.println(String.format("[JAVA-TIME] hash done. \t%s", tm.elapsedTimeString()));
	}

}
