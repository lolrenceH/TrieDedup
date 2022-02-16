# Custom class of the trie (prefix tree) node: TrieNode
# the recursive algorithm for checking if a query sequence exists in the input trie
# @Author : Jianqiao Hu & Adam Yongxin Ye @ BCH


# JH 020322 testing v2 v3 collapseSeq ——> two ways of using list comprehension to drop exact,  filter and sort Ns
import sys

from lib.restrictedDict import restrictedListDict
import numpy as np
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


def collapseSeq(seqs, allowed_symbols='ACGTN', ambiguous_symbols='N', is_input_sorted=False, max_missing=500,
                should_benchmark_memory=False, verbose=False):
    """
    Removes duplicate sequences

    Arguments:
      seqs : the input sequences
      allowed_symbols : the list of allowed symbols, such as bases 'ACGTN'
      ambiguous_symbols: the list of ambiguous symbols, such as 'N'
      is_input_sorted : is the input seqs already sorted by num_N; if not, I will sort in this function
      max_missing : number of ambiguous characters to allow in a unique sequence.
      should_benchmark_memory : benchmark memory usage or not.

    Returns:
      is_uniq_vec, time cost, [memory usage]
    """
    hp = None
    if should_benchmark_memory:
        hp = hpy()
    start_time = timeit.default_timer()
    restrictedListDict.addAllowedKeys(allowed_symbols)
    trie = TrieNode()

    if len(ambiguous_symbols) > 1:  # convert all ambiguous symbols to ambiguous_symbols[0]
        for ch in ambiguous_symbols[1:]:
            seqs = [seq.replace(ch, ambiguous_symbols[0]) for seq in seqs]
    if verbose:
        print(f"[NOTE] Number of reads (raw) = {len(seqs)}", file=sys.stderr)
    unique_seqs = list(set(seqs))
    if verbose:
        print(f"[NOTE] Number of reads (without exact matches) = {len(unique_seqs)}", file=sys.stderr)

    unique_seqs_filtered = [u_s for u_s in unique_seqs if u_s.count('N') <= max_missing]
    unique_seqs_Nfiltered_sorted = unique_seqs_filtered
    if not is_input_sorted:
        if verbose:
            print(f"[NOTE] sorting...",file=sys.stderr)
        unique_seqs_Nfiltered_sorted.sort(key=lambda x: x.count('N'))
    if verbose:
        print( f"[NOTE] Number of reads (without exact matches) that have {max_missing} N or less = {len(unique_seqs_Nfiltered_sorted)}", file=sys.stderr)

    TIMESPENT2 = timeit.default_timer() - start_time
    if verbose:
        print(f"[NOTE] collapseSeq preprocess (filter, sort) done. Time spent: {TIMESPENT2} s", file=sys.stderr)

    uniq_dict = {}
    for si in range(len(unique_seqs_Nfiltered_sorted)):
        seq = unique_seqs_Nfiltered_sorted[si]
        if not trie.search(seq):  # not found
            trie.add(seq)
            uniq_dict[seq] = True

    TIMESPENT = timeit.default_timer() - start_time
    if should_benchmark_memory:
        h = hp.heap()
    is_uniq_vec = [0] * len(seqs)
    for i in range(len(seqs)):
        if seqs[i] in uniq_dict:
            is_uniq_vec[i] = 1
            del uniq_dict[seqs[i]]
    if should_benchmark_memory:
        return [is_uniq_vec, TIMESPENT, h]
    return [is_uniq_vec, TIMESPENT]

