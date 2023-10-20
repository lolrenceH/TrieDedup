package edu.harvard.hms.triededup.utils;

public enum ACGTNEnum {
	A (0),
	C (1),
	G (2),
	T (3),
	N (4);
	
	private final int idx;
	
	ACGTNEnum(int idx) {
		this.idx = idx;
	}
	
	public int getIdx() {
		return this.idx;
	}
	
	static public int char2idx(char ch){
		int ans = -1;
		switch(ch){
		case 'A':
			ans = 0;
			break;
		case 'C':
			ans = 1;
			break;
		case 'G':
			ans = 2;
			break;
		case 'T':
			ans = 3;
			break;
		case 'N':
			ans = 4;
			break;
		}
		return ans;
	}
	
	static public char idx2char(int i){
		char ans = 'X';
		switch(i){
		case 0:
			ans = 'A';
			break;
		case 1:
			ans = 'C';
			break;
		case 2:
			ans = 'G';
			break;
		case 3:
			ans = 'T';
			break;
		case 4:
			ans = 'N';
			break;
		}
		return ans;
	}
}
