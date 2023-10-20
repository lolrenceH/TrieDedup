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
 * A class imitating a HashMap, store values in a ArrayList, with restricted
 * keys
 * 
 * @author Adam Yongxin Ye @ BCH
 *
 */
@SuppressWarnings("rawtypes")
public class RestrictedMap implements Map {

	// Note: cannot declare statis List<T> !   ref: https://docs.oracle.com/javase/tutorial/java/generics/restrictions.html , https://docs.oracle.com/javase/tutorial/java/generics/types.html
	static List allowed_keys = new ArrayList();
	static Map<Object, Integer> key2idx = new HashMap<Object, Integer>();
	static Object default_value = null;

	static public void addAllowedKeys(Collection keys) {
		for(Object x : keys){
			if(! key2idx.containsKey(x)){
				int prevLen = allowed_keys.size();
				allowed_keys.add(x);
				key2idx.put(x, prevLen);
			}
		}
	}

	static public void setDefaultValue(Object value) {
		default_value = value;
	}

	static public RestrictedMap fromkeys(Collection keys, Object value) {
		RestrictedMap ans = new RestrictedMap();
		for(Object key : keys){
			ans.put(key, value);
		}
		return ans;
	}

	static public RestrictedMap fromkeys(Collection keys) {
		return RestrictedMap.fromkeys(keys, null);
	}

	private List storage;

	public RestrictedMap() {
		super();
		this.storage = new ArrayList();
	}

	@Override
	public int size() {
		return this.storage.size();
		// simply the length of storage list, not actual how many stored keys
	}

	@Override
	public boolean isEmpty() {
		return this.values().isEmpty();
	}

	@Override
	public boolean containsKey(Object key) {
		if(RestrictedMap.key2idx.containsKey(key)){
			int idx = RestrictedMap.key2idx.get(key);
			if(this.storage.size() > idx){
				if(this.storage.get(idx) != null){
					return true;
				}
			}
		}
		return false;
	}

	@Override
	public boolean containsValue(Object value) {
		return this.storage.contains(value);
	}

	@Override
	public Object get(Object key) throws IndexOutOfBoundsException {
		if(RestrictedMap.key2idx.containsKey(key)){
			int idx = RestrictedMap.key2idx.get(key);
			if(this.storage.size() > idx){
				return this.storage.get(idx);
			}else{
				return null;
			}
		}else{
			throw new IndexOutOfBoundsException(String.format("Key %s is not allowed", key));
		}
	}
	public Object get(Object key, Object defaultvalue) throws IndexOutOfBoundsException {
		Object ans = this.get(key);
		if(ans == null){
			if(defaultvalue == null){
				defaultvalue = RestrictedMap.default_value;
				// TODO: orignal python code designated to make a deep copy 
				//       and weirdly modified storage to insert the default value
			}
			return defaultvalue;
		}
		return ans;
	}
	
	@Override
	public Object put(Object key, Object value) throws IndexOutOfBoundsException {
		if(RestrictedMap.key2idx.containsKey(key)){
			int idx = RestrictedMap.key2idx.get(key);
			int prevLen = this.storage.size();
			if(prevLen <= idx){
				// extend the storage list if necessary, fill in None
				for(int i=prevLen; i<=idx; i++){
					this.storage.add(null);
				}
			}
			Object prevValue = this.storage.get(idx);
			this.storage.set(idx, value);
			return prevValue;
		}else{
			throw new IndexOutOfBoundsException(String.format("Key %s is not allowed", key));
		}
	}

	@Override
	public Object remove(Object key) {
		if(RestrictedMap.key2idx.containsKey(key)){
			int idx = RestrictedMap.key2idx.get(key);
			int prevLen = this.storage.size();
			if(prevLen > idx){
				Object prevValue = this.storage.get(idx);
				this.storage.set(idx, null);
				return prevValue;
			}else{
				return null;
			}
		}else{
			throw new IndexOutOfBoundsException(String.format("Key %s is not allowed", key));
		}
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
		this.storage = new ArrayList();
	}

	@Override
	public Set keySet() {
		Set ans = new HashSet();
		for(int i=0; i<this.storage.size(); i++){
			if(this.storage.get(i) != null){
				ans.add(RestrictedMap.allowed_keys.get(i));
			}
		}
		return ans;
	}

	@Override
	public Collection values() {
		Set ans = new HashSet();
		for(int i=0; i<this.storage.size(); i++){
			Object value = this.storage.get(i);
			if(value != null){
				ans.add(value);
			}
		}
		return ans;
	}

	@Override
	public Set entrySet() {
		Set<Map.Entry> ans = new HashSet<Map.Entry>();
		for(int i=0; i<this.storage.size(); i++){
			Object value = this.storage.get(i);
			if(value != null){
				Object key = RestrictedMap.allowed_keys.get(i);
				ans.add(new AbstractMap.SimpleEntry(key, value));
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
