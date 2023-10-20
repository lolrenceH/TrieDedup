/**
 * 
 */
package edu.harvard.hms.triededup.utils;

import java.util.Map;
import java.util.Set;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.AbstractMap;
import java.util.ArrayList;
import java.util.Collection;

/**
 * A class like RestrictedMap, but hard-coded for ACGTN
 * 
 * @author Adam Yongxin Ye @ BCH
 *
 */
@SuppressWarnings("rawtypes")
public class ACGTNMap implements Map {

//	static final char[] allowed_keys = new char[] {'A', 'C', 'G', 'T', 'N'};   // hard-coded

	static public ACGTNMap fromkeys(Collection<Character> keys, Object value) {
		ACGTNMap ans = new ACGTNMap();
		for(Character key : keys){
			ans.put(key, value);
		}
		return ans;
	}

	static public ACGTNMap fromkeys(Collection keys) {
		return ACGTNMap.fromkeys(keys, null);
	}

	static final int keys_size = ACGTNEnum.values().length;
	
	private Object[] storage;
	private int storage_size;

	public ACGTNMap() {
		super();
		this.clear();
	}

	@Override
	public int size() {
//		return keys_size;   // simply the length of storage list, not actual how many stored keys
		return this.storage_size;
	}

	@Override
	public boolean isEmpty() {
		return this.values().isEmpty();
	}

	public boolean containsKey(char key) {
		int idx = ACGTNEnum.char2idx(key);
		if(idx >= 0){
			if(this.storage[idx] != null){
				return true;
			}
		}
		return false;
	}
	@Override
	public boolean containsKey(Object key) {
		return this.containsKey(((Character)key).charValue());
	}

	@Override
	public boolean containsValue(Object value) {
		for(int i=0; i<keys_size; i++){
			if(this.storage[i].equals(value)){
				return true;
			}
		}
		return false;
	}

	public Object get(char key) throws IndexOutOfBoundsException {
		int idx = ACGTNEnum.char2idx(key);
		if(idx >= 0){
			return this.storage[idx];
		}else{
			throw new IndexOutOfBoundsException(String.format("Key %s is not allowed", key));
		}
	}
	@Override
	public Object get(Object key) throws IndexOutOfBoundsException {
		return this.get(((Character)key).charValue());
	}
	public Object get(Object key, Object defaultvalue) throws IndexOutOfBoundsException {
		Object ans = this.get(key);
		if(ans == null){
			return defaultvalue;
		}
		return ans;
	}
	
	public Object put(char key, Object value) throws IndexOutOfBoundsException {
		int idx = ACGTNEnum.char2idx(key);
		if(idx >= 0){
			Object prevValue = this.storage[idx];
			this.storage[idx] = value;
			if(prevValue == null){
				this.storage_size++;
			}
			return prevValue;
		}else{
			throw new IndexOutOfBoundsException(String.format("Key %s is not allowed", key));
		}
	}
	@Override
	public Object put(Object key, Object value) throws IndexOutOfBoundsException {
		return this.put(((Character)key).charValue(), value);
	}

	public Object remove(char key) {
		int idx = ACGTNEnum.char2idx(key);
		if(idx >= 0){
			Object prevValue = this.storage[idx];
			this.storage[idx] = null;
			if(prevValue != null){
				this.storage_size--;
			}
			return prevValue;
		}else{
			throw new IndexOutOfBoundsException(String.format("Key %s is not allowed", key));
		}
	}
	@Override
	public Object remove(Object key) {
		return this.remove(((Character)key).charValue());
	}

	@Override
	public void putAll(Map m) {
		Iterator<Map.Entry> iter = m.entrySet().iterator();
		while(iter.hasNext()){
			Map.Entry entry = iter.next();
			this.put(entry.getKey(), entry.getValue());
		}
	}

	@Override
	public void clear() {
		this.storage = new Object[keys_size];
		this.storage_size = 0;
	}

	@Override
	public Set keySet() {
		Set<Character> ans = new HashSet<Character>();
		for(int i=0; i<keys_size; i++){
			if(this.storage[i] != null){
				ans.add(ACGTNEnum.idx2char(i));
			}
		}
		return ans;
	}

	@Override
	public Collection values() {
		Set ans = new HashSet();
		for(int i=0; i<keys_size; i++){
			Object value = this.storage[i];
			if(value != null){
				ans.add(value);
			}
		}
		return ans;
	}

	@Override
	public Set entrySet() {
		Set<Map.Entry> ans = new HashSet<Map.Entry>();
		for(int i=0; i<keys_size; i++){
			Object value = this.storage[i];
			if(value != null){
				char key = ACGTNEnum.idx2char(i);
				ans.add(new AbstractMap.SimpleEntry((Character)key, value));
			}
		}
		return ans;
	}
	public List<Map.Entry<Character, Object>> entryList() {
		List<Map.Entry<Character, Object>> ans = new ArrayList<Map.Entry<Character, Object>>();
		for(int i=0; i<keys_size; i++){
			Object value = this.storage[i];
			if(value != null){
				char key = ACGTNEnum.idx2char(i);
				ans.add(new AbstractMap.SimpleEntry((Character)key, value));
			}
		}
		return ans;
	}
	
	@Override
	public String toString() {
		List<String> vec = new ArrayList<String>();
		Iterator<Map.Entry> iter = this.entrySet().iterator();
		while(iter.hasNext()){
			Map.Entry entry = iter.next();
			vec.add(String.format("%s : %s", entry.getKey(), entry.getValue()));
		}
		return String.format("{%s}", String.join(", ", vec));
	}
	
	// TODO: orignal python code also has deep copy method?
}
