package edu.harvard.hms.triededup.utils;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * A util class to parse sequences from input file
 *   each read_* function will return a list of two lists with same length
 *     (1) sequence names, (2) sequences
 * 
 * @author Adam Yongxin Ye & Jianqiao Hu @ BCH
 *
 */
public class SequencesReader {
	public static List<SeqIdAndSeq> read_fasta(String input_path) throws IOException{
		List<SeqIdAndSeq> seqs_vec = new ArrayList<SeqIdAndSeq>();
		System.err.println(String.format("[STEP] opening fasta file %s ...", input_path));
		BufferedReader reader = new BufferedReader(new FileReader(input_path));
		String now_name = "";
		StringBuilder now_seq = new StringBuilder();
		String line;
		while((line = reader.readLine()) != null){
			line = line.trim();   // may change to stripTrailing after Java 11
			if(line.charAt(0) == '>'){
				if(now_name != ""){
					now_name = now_name.split(" ")[0];
					seqs_vec.add(new SeqIdAndSeq(now_name, now_seq.toString()));
				}
				now_name = line.substring(1);
				now_seq = new StringBuilder();
			}else{
				now_seq.append(line.toUpperCase());
			}
		}
		if(now_name != ""){
			seqs_vec.add(new SeqIdAndSeq(now_name, now_seq.toString()));
		}
		reader.close();
		
		return seqs_vec;
	}
}
