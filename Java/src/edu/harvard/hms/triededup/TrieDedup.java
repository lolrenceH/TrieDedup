/**
 * 
 */
package edu.harvard.hms.triededup;

import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

import edu.harvard.hms.triededup.utils.Deduper;
import edu.harvard.hms.triededup.utils.SeqIdAndSeq;
import edu.harvard.hms.triededup.utils.YyxTimer;

/**
 * @author Yyx26
 *
 */
public class TrieDedup {
	
	public static String getFileExtension(String filename){
		int idx = filename.lastIndexOf(".");
		if(idx > -1){
			return filename.substring(idx + 1);
		}else{
			return "";
		}
	}
	/**
	 * @param args
	 * @throws InterruptedException 
	 * @throws IOException 
	 * @throws ParseException 
	 */
	public static void main(String[] args) throws InterruptedException, IOException, ParseException {
		// java-commonss-cli   ref: https://opensource.com/article/21/8/java-commons-cli , https://www.tutorialspoint.com/commons_cli/commons_cli_quick_guide.htm
		Options options = new Options();
		Option opthelp = new Option("h", "help", false, "show this command-line help page");
		options.addOption(opthelp);
		Option optout = Option.builder("o").longOpt("output")
				.hasArg().argName("file")
				.desc("set output file path (default: STDOUT)").build();
		options.addOption(optout);
		Option optsorted = new Option("s", "sorted", false, "input already uniq and sorted (default: false)");
		options.addOption(optsorted);
		Option optmaxN = Option.builder("m").longOpt("max-missing")
				.hasArg().argName("int")
				.desc("max number of Ns allowed for each read (default: 9999)").build();
		options.addOption(optmaxN);
		Option optminbaseQ = Option.builder("q").longOpt("min-baseQ")
				.hasArg().argName("int")
				.desc("bases with lower baseQ will be converted to N (default: 0)").build();
		options.addOption(optminbaseQ);
		Option optbaseQshift = Option.builder("t").longOpt("baseQ-shift")
				.hasArg().argName("int")
				.desc("baseQ value shifted from char (default: 33)").build();
		options.addOption(optbaseQshift);
		
		CommandLineParser parser = new DefaultParser();
		HelpFormatter helper = new HelpFormatter();
		
		String version = "\nVersion: 0.1.2 (2022-10-21)\n"
				+ "Author: Adam Yongxin Ye & Jianqiao Hu @ BCH\n";
		String usage = "\nUsage: java -jar TrieDedup.jar <command> <input>\n"
				+ version
				+ "\nSupported <command>:"
				+ "\n    sortuniq \tjust uniq by sequence and sort by N, and output fasta"
				+ "\n    trie \tdeduplicate using trie algorithm"
				+ "\n    pairwise \tdeduplicate using pairwise algorithm\n"
				+ "\nSupported <input> format:"
//				+ "\t.fasta, .fa,  .fastq, .fq,  .sam, .bam, .cram"
				+ "\n    (automatically determined by <input>'s file extension)"
				+ "\t.fasta, .fa,  .fastq, .fq,  .sam, .bam, .cram\n"
				+ "\nOutput:  STDOUT  or  -o|--output <file>\tin fasta format\n";
		
		YyxTimer all_tm = new YyxTimer();
		
		YyxTimer tm = new YyxTimer();
		System.err.print(String.format("[STEP] parsing command-line arguments ..."));
		
		CommandLine cmd = parser.parse(options, args);			
		
		if(cmd.hasOption("h")){
			helper.printHelp(usage + "\nOptions:", options);
			System.exit(-1);
		}
		
		args = cmd.getArgs();
//		System.err.println(String.format("args = {%s}", String.join(", ", args)));
		if(args.length < 2){
			System.err.println("\nError: not enough command-line arguments, need <command> and <input>");
			helper.printHelp(usage + "\nOptions:", options);
			System.exit(-1);
		}
		
		String command_choose = args[0];
		String input_filename = args[1];
		
		int max_missing = 9999;
		if(cmd.hasOption("m")){
			max_missing = Integer.parseInt(cmd.getOptionValue("m"));
		}
		boolean is_input_sorted = false;
		if(cmd.hasOption("s")){
			is_input_sorted = true;
		}
		int min_baseQ = 0;
		if(cmd.hasOption("q")){
			min_baseQ = Integer.parseInt(cmd.getOptionValue("q"));
		}
		int baseQ_shift = 33;
		if(cmd.hasOption("t")){
			baseQ_shift = Integer.parseInt(cmd.getOptionValue("t"));
		}
		String output_filename = "STDOUT";
		if(cmd.hasOption("o")){
			output_filename = cmd.getOptionValue("o");
		}
		
		PrintStream out = System.out;
//		if(args.length > 4){
//			output_filename = args[4];
		if(! output_filename.equals("STDOUT")){
			out = new PrintStream(output_filename);
		}
//		}

//		Thread.sleep(1000);
		System.err.println(String.format(" \t%s", tm.elapsedTimeString()));
		System.err.println(String.format("  Current working directory = %s", System.getProperty("user.dir")));
		System.err.println(String.format("[ARG] command_choose = %s", command_choose));
		System.err.println(String.format("[ARG] input_filename = %s", input_filename));
		System.err.println(String.format("[OPT] sorted = %s", is_input_sorted));
		System.err.println(String.format("[OPT] max_missing = %d", max_missing));
		System.err.println(String.format("[OPT] baseQ_shift = %d", baseQ_shift));
		System.err.println(String.format("[OPT] min_baseQ = %d", min_baseQ));
		
		if(command_choose.equals("trie")){
			// good
		}else if(command_choose.equals("pairwise")){
			// good
		}else if(command_choose.equals("sortuniq")){
			// good
		}else{
			System.err.println(String.format("Error: unknown function = %s\n", command_choose));
			System.err.println(usage);
			System.exit(-1);
		}
		
		// call SequenceReader to parse the input file to a list of names and sequences
		List<SeqIdAndSeq> parsed_id_seqs = new ArrayList<SeqIdAndSeq>();
		String input_file_extension = TrieDedup.getFileExtension(input_filename);
		tm.resetTime();
		if(input_file_extension.equals("fa") || input_file_extension.equals("fasta")){
			System.err.println(String.format("[STEP] reading sequences in fasta ..."));
			parsed_id_seqs = SeqIdAndSeq.read_fasta(input_filename);
		}else if(input_file_extension.equals("fq") || input_file_extension.equals("fastq")){
			System.err.println(String.format("[STEP] reading sequences in fastq ..."));
			parsed_id_seqs = SeqIdAndSeq.read_fastq(input_filename, min_baseQ, -baseQ_shift);
		}else if(input_file_extension.equals("sam") || input_file_extension.equals("bam") || input_file_extension.equals("cram")){
			System.err.println(String.format("[STEP] reading sequences in sam/bam/cram ..."));
			parsed_id_seqs = SeqIdAndSeq.read_bam(input_filename, min_baseQ, -baseQ_shift+33);
		}else{
			System.err.println(String.format("Error: cannot parse input file with extension '%s'", input_file_extension));
			System.exit(-2);
		}
		System.err.println(String.format("[STEP-TIME] reading %d sequences done. \t%s", parsed_id_seqs.size(), tm.elapsedTimeString()));
		
		List<SeqIdAndSeq> uniq_id_seqs = parsed_id_seqs;
		if(! is_input_sorted){
			// uniq_and_sort
			tm.resetTime();
			System.err.println(String.format("[STEP] uniq and sort by N ..."));
			uniq_id_seqs = Deduper.uniq_and_sort(parsed_id_seqs, false, max_missing);
			System.err.println(String.format("[STEP-TIME] uniq and sort done. \t%s", tm.elapsedTimeString()));
			System.err.println(String.format("[NOTE] Uniq and sort resulted in %d unique reads.", uniq_id_seqs.size()));
		}
		
		if(! command_choose.equals("sortuniq")){   // need deduplication
			// deduplication
	//		List<SeqIdAndSeq> dedup_id_seqs = new ArrayList<SeqIdAndSeq>();
			tm.resetTime();
			if(command_choose.equals("trie")){
				System.err.println(String.format("[STEP] deduplicating by trie ..."));
				uniq_id_seqs = Deduper.collapseSeqTrie(uniq_id_seqs);
			}else if(command_choose.equals("pairwise")){
				System.err.println(String.format("[STEP] deduplicating by pairwise ..."));
				uniq_id_seqs = Deduper.collapseSeqPairwise(uniq_id_seqs);
			}
			System.err.println(String.format("[STEP-TIME] deduplication done. \t%s", tm.elapsedTimeString()));
			System.err.println(String.format("[NOTE] Deduplicating resulted in %d unique reads.", uniq_id_seqs.size()));
		}
		
		// output
		tm.resetTime();
		System.err.println(String.format(String.format("[STEP] output to %s ...", output_filename)));
//		for(String seqId : dedup_ans){
//			out.println(seqId);
//		}
		SeqIdAndSeq.write_fasta(out, uniq_id_seqs);
		if(! output_filename.equals("STDOUT")){
			out.close();
		}
		System.err.println(String.format("[STEP-TIME] output done. \t%s", tm.elapsedTimeString()));

		System.err.println(String.format("[ALL-TIME] all done. \t%s", all_tm.elapsedTimeString()));
	}

}
