package edu.harvard.hms.triededup.utils;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;

import htsjdk.samtools.SAMRecord;
import htsjdk.samtools.SamReader;
import htsjdk.samtools.SamReaderFactory;
import htsjdk.samtools.ValidationStringency;

/**
 * A structure class to store one pair of sequence ID and its sequence
 * 
 * @author Adam Yongxin Ye @ BCH
 *
 */
public class SeqIdAndSeq {
	public String seqId;
	public String sequence;
	
	public SeqIdAndSeq(String seqId, String sequence){
		this.seqId = seqId;
		this.sequence = sequence;
	}
	
	
	public static void write_fasta(PrintStream out, List<SeqIdAndSeq> id_seqs){
		for(SeqIdAndSeq id_seq : id_seqs){
			out.print('>');
			out.println(id_seq.seqId);
			out.println(id_seq.sequence);
		}
	}
	
	
	public static List<SeqIdAndSeq> read_fasta(String input_path) throws IOException{
		List<SeqIdAndSeq> id_seqs = new ArrayList<SeqIdAndSeq>();
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
					id_seqs.add(new SeqIdAndSeq(now_name, now_seq.toString()));
				}
				now_name = line.substring(1);
				now_seq = new StringBuilder();
			}else{
				now_seq.append(line.toUpperCase());
			}
		}
		if(now_name != ""){
			id_seqs.add(new SeqIdAndSeq(now_name, now_seq.toString()));
		}
		reader.close();
		
		return id_seqs;
	}
	
	public static List<SeqIdAndSeq> read_fastq(String input_path, int min_baseQ, int baseQ_coding_shift) throws IOException{
		List<SeqIdAndSeq> id_seqs = new ArrayList<SeqIdAndSeq>();
		System.err.println(String.format("[STEP] opening fastq file %s ...", input_path));
		BufferedReader reader = new BufferedReader(new FileReader(input_path));
		String now_name = "";
		char[] now_seq;
		String[] lines = new String[4];
		int NR = 1;
		while((lines[0] = reader.readLine()) != null){
			lines[1] = reader.readLine();
			lines[2] = reader.readLine();
			lines[3] = reader.readLine();
			if(lines[1] == null){
				break;
			}
			lines[0] = lines[0].trim();   // may change to stripTrailing after Java 11
			lines[1] = lines[1].trim();
			lines[3] = lines[3].trim();
			
			if(lines[0].charAt(0) == '@'){
				now_name = lines[0].substring(1);
				now_seq = lines[1].toCharArray();
				
				if(min_baseQ > 0){
					// convert bases with lower baseQ to Ns
					if(lines[1].length() != lines[3].length()){
						System.err.println(String.format("Warning: invalid fastq format: different length of bases and baseQs at Line %d and %d", (NR+1), (NR+3)));
					}
					int len = lines[1].length();
					if(lines[3].length() < len){
						len = lines[3].length();
					}
					for(int i=0; i<len; i++){
						if(lines[3].charAt(i) + baseQ_coding_shift < min_baseQ){
							now_seq[i] = 'N';
						}
					}
				}
				
				id_seqs.add(new SeqIdAndSeq(now_name, new String(now_seq)));
			}else{
				System.err.println(String.format("Warning: invalid fastq format: first line not start with @ for Line %d", NR));
			}
			NR += 4;
		}
		reader.close();
		
		return id_seqs;
	}
	
	public static List<SeqIdAndSeq> read_bam(String input_path, int min_baseQ, int baseQ_coding_shift) throws IOException{
		List<SeqIdAndSeq> id_seqs = new ArrayList<SeqIdAndSeq>();
		System.err.println(String.format("[STEP] opening sam/bam/cram file %s ...", input_path));
		// htsjdk   ref: https://github.com/samtools/htsjdk/blob/master/src/main/java/htsjdk/samtools/example/ExampleSamUsage.java
		final SamReader reader = SamReaderFactory.makeDefault().validationStringency(ValidationStringency.LENIENT).open(new File(input_path));
		int NR = 1;
		for(final SAMRecord samRecord : reader){
			char[] now_seq = samRecord.getReadString().toCharArray();
			byte[] now_baseQs = samRecord.getBaseQualities();

			if(min_baseQ > 0){
				// convert bases with lower baseQ to Ns
				if(now_seq.length != now_baseQs.length){
					System.err.println(String.format("Warning: invalid sam/bam/cram format: different length of bases and baseQs at Line %d", NR));
				}
				int len = now_seq.length;
				if(now_baseQs.length < len){
					len = now_baseQs.length;
				}
				for(int i=0; i<len; i++){
					if(now_baseQs[i] + baseQ_coding_shift < min_baseQ){
						now_seq[i] = 'N';
					}
				}
			}
			
			id_seqs.add(new SeqIdAndSeq(samRecord.getReadName(), new String(now_seq)));
			
			NR++;
		}
		reader.close();
		
		return id_seqs;
	}
	
	
}
