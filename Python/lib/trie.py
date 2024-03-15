# Custom class of the trie (prefix tree) node: TrieNode
# the recursive algorithm for checking if a query sequence exists in the input trie
# @Author : Jianqiao Hu & Adam Yongxin Ye @ BCH


# JH 020322 testing v2 v3 collapseSeq ——> two ways of using list comprehension to drop exact,  filter and sort Ns
import sys

from lib.restrictedDict import restrictedListDict
from collections.abc import Set
import timeit

class TrieNode(Set):
    """
    Initialize data structure here
    """
    __slots__ = '_keys', '_child', '_end'

    def __init__(self, iterable=()):
        self._keys = []   # bases stored in this node, a list of the keys of dict ._child; keep 'N' at the last element
        self._child = restrictedListDict()   # a dict of TrieNode; values are TrieNode, keys are the bases also stored in _keys
        self._end = False   # set this flag for the child node of the end base of sequence
        for element in iterable:
            self.add(element)

    def __contains__(self, element):
        """
        Check if self contains the element (sequence) as an entire child
        """
        node = self
        for k in element:
            if k not in node._keys:
                return False
            node = node._child[k]
        return node._end

    def __iter__(self):
        """
        Return an iterator of all the sequences from this node
        """
        element = ['']
        stack = [iter([('', self)])]
        while stack:
            for k, node in stack[-1]:
                element.append(k)
                if node._end:
                    yield ''.join(element)
                stack.append(iter(node._child.items()))
                break
            else:
                element.pop()
                stack.pop()

    def __len__(self):
        """
        Return the number of the sequences from this node
        """
        return sum(1 for _ in self)

    def add(self, sequence):
        """
        Add a sequence from this node
        """
        node = self
        for base in sequence:
            if base not in node._keys:
                if len(node._keys) > 0 and node._keys[-1] == 'N':
                    # keep 'N' at the last element of _keys
                    node._keys.insert(len(node._keys) - 1, base)
                else:
                    node._keys.append(base)
                #
                node._child[base] = TrieNode()
            node = node._child[base]
        node._end = True

    def search(self, sequence, i=0):
        """
        Search for any match of sequence[i:] starting at node self
        """
        # Assume sequence[:i] has already matched, search for sequence[i:] starting at node self
        if i == len(sequence):
            if self._end:
                return True
        else:
            for base in self._keys:
                if sequence[i] == base or sequence[i] == 'N' or base == 'N':
                    if self._child[base].search(sequence, i + 1):
                        return True
        return False

    def search_with_traceback(self, sequence, i=0):
        """
        Search for any match of sequence[i:] starting at node self
        """
        # Assume sequence[:i] has already matched, search for sequence[i:] starting at node self
        if i == len(sequence):
            if self._end:
                return ''
        else:
            for base in self._keys:
                if sequence[i] == base or sequence[i] == 'N' or base == 'N':
                    ans =  self._child[base].search_with_traceback(sequence, i + 1)
                    if ans is not None:
                        return base + ans
        return None


def collapseSeq(seqs, allowed_symbols='ACGTN', ambiguous_symbols='N', is_input_sorted=False, max_missing=500,
                hp=None, should_just_uniq_sort=False, should_traceback=False):
    """
    Removes duplicate sequences

    Arguments:
      seqs : the input sequences
      allowed_symbols : the list of allowed symbols, such as bases 'ACGTN'
      ambiguous_symbols: the list of ambiguous symbols, such as 'N'
      is_input_sorted : is the input seqs already sorted by num_N; if not, I will sort in this function
      max_missing : number of ambiguous characters to allow in a unique sequence.
      hp : hyp() object for memory benchmarking.
      should_just_uniq_sort : just do uniq of exact matching and sort by number of Ns
      should_traceback : should I return mapping_vec instead of uniqIdx_vec?

    Returns:
      uniqIdx_vec, time cost, [memory usage]
      (or mapping_vec, time cost, [memory usage] if should_traceback=True)
          mapping_vec[i] = -1 if seqs[i] is discarded
          mapping_vec[i] = j  if seqs[i] is duplicates of j (j=i means uniq)
    """
    start_time = timeit.default_timer()
    restrictedListDict.addAllowedKeys(allowed_symbols)
    trie = TrieNode()
    
    if len(ambiguous_symbols) > 1:  # convert all ambiguous symbols to ambiguous_symbols[0]
        for ch in ambiguous_symbols[1:]:
            seqs = [seq.replace(ch, ambiguous_symbols[0]) for seq in seqs]
    print(f"[NOTE] Number of reads (raw) = {len(seqs)}", file=sys.stderr)
    
    if should_traceback:
        mapping_vec = [-1] * len(seqs)
        uniqIdx2idxes = dict()
    seq2uniqIdx = dict()
    for idx, seq in enumerate(seqs):
        uniqIdx = idx
        if seq in seq2uniqIdx:
            uniqIdx = seq2uniqIdx[seq]
        else:
            seq2uniqIdx[seq] = idx
        if should_traceback:
            mapping_vec[idx] = uniqIdx
            if uniqIdx not in uniqIdx2idxes:
                uniqIdx2idxes[uniqIdx] = []
            uniqIdx2idxes[uniqIdx].append(idx)
    unique_seqs = list(seq2uniqIdx.keys())
    print(f"[NOTE] Number of reads (filtering out exact matches) = {len(unique_seqs)}", file=sys.stderr)

    if should_traceback:
        unique_seqs_filtered = []
        for idx, seq in enumerate(seqs):
            uniqIdx = seq2uniqIdx[seq]
            if idx == uniqIdx:   # unique_seqs
                if seq.count(ambiguous_symbols[0]) <= max_missing:   # unique_seqs_filtered
                    unique_seqs_filtered.append(seq)
                else:
                    for now_idx in uniqIdx2idxes[uniqIdx]:
                        mapping_vec[now_idx] = -1   # filtered out due to too many Ns
    else:
        unique_seqs_filtered = [u_s for u_s in unique_seqs if u_s.count(ambiguous_symbols[0]) <= max_missing]
    
    unique_seqs_Nfiltered_sorted = unique_seqs_filtered
    if not is_input_sorted:
        print(f"[NOTE] sorting...",file=sys.stderr)
        unique_seqs_Nfiltered_sorted.sort(key=lambda x: x.count(ambiguous_symbols[0]))
    print( f"[NOTE] Number of reads (filtering out exact matches) that have {max_missing} N or less = {len(unique_seqs_Nfiltered_sorted)}", file=sys.stderr)

    # TIMESPENT2 = timeit.default_timer() - start_time
    # print(f"[NOTE] collapseSeq_v2 drop, filter, sort {TIMESPENT2}", file=sys.stderr)

#    uniq_dict = {}
    uniqIdx_vec = []
    if should_just_uniq_sort:
        for seq in unique_seqs_Nfiltered_sorted:
            uniqIdx_vec.append(seq2uniqIdx[seq])
    else:
        if should_traceback:
            for seq in unique_seqs_Nfiltered_sorted:
                matched_seq = trie.search_with_traceback(seq)
                if matched_seq is None:   # not found, uniq after TrieDedup
                    trie.add(seq)
                else:   # seq is duplicates of matched_seq
                    uniqIdx = seq2uniqIdx[seq]
                    for now_idx in uniqIdx2idxes[uniqIdx]:
                        mapping_vec[now_idx] = seq2uniqIdx[matched_seq]
#                        uniqIdx2idxes[seq2uniqIdx[matched_seq]].append(now_idx)   # skip this because trie dedup is the last step; otherwise, uncomment this line
        else:
            for seq in unique_seqs_Nfiltered_sorted:
                if not trie.search(seq):  # not found, uniq after TrieDedup
                    trie.add(seq)
                    uniqIdx_vec.append(seq2uniqIdx[seq])
#                    uniq_dict[seq] = True

#    print(f'uniqIdx_vec[1:5] = {uniqIdx_vec[1:5]}', file=sys.stderr)
    TIMESPENT = timeit.default_timer() - start_time
    if hp:
        h = hp.heap()
#    is_uniq_vec = [0] * len(seqs)
#    for i in range(len(seqs)):
#        if seqs[i] in uniq_dict:
#            is_uniq_vec[i] = 1
#            del uniq_dict[seqs[i]]
    if should_traceback:
        if hp:
            return [mapping_vec, TIMESPENT, h]
        return [mapping_vec, TIMESPENT]
        
    if hp:
        return [uniqIdx_vec, TIMESPENT, h]
    return [uniqIdx_vec, TIMESPENT]

