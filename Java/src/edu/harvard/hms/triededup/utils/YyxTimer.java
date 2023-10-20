package edu.harvard.hms.triededup.utils;

/**
 * A class dealing with benchmarking elapsed time
 * 
 * @author Adam Yongxin Yes @ BCH
 *
 */
public class YyxTimer {
	private long start_time;
	
	public YyxTimer(){
		start_time = System.nanoTime();
	}
	
	public long startTime(){
		return this.start_time;
	}
	
	public void resetTime(){
		start_time = System.nanoTime();
	}
	
	public long currentTime(){
		return System.nanoTime();
	}
	
	public long elapsedTime(){
		return System.nanoTime() - this.start_time;
	}
	
	public String elapsedTimeString(){
		return YyxTimer.formatElapsedTime(this.elapsedTime());
	}
	
	public static String formatElapsedTime(long elapsedNanoSeconds){
		double elapsedSeconds = elapsedNanoSeconds / 1.0e9;
		int day = (int)(elapsedSeconds / (3600*24));
		int hour = (int)(elapsedSeconds % (3600*24) / 3600);
		int min = (int)(elapsedSeconds % 3600 / 60);
		double sec = (double)(elapsedSeconds % 60);
		StringBuilder sb = new StringBuilder();
		if(day > 0){
			sb.append(day);
			sb.append("day ");
		}
		if(hour > 0){
			sb.append(hour);
			sb.append("h");
		}
		if(min > 0){
			sb.append(min);
			sb.append("min");
		}
		if(sec > 0){
			sb.append(String.format("%.7f", sec));
			sb.append("s");
		}
		return sb.toString();
	}
}
