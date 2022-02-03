# Progressive pairwise comparison algorithm retrived from pRESTO
# we simplified it and added some code for benchmarking the time cost and memory usage
# @Author : Jianqiao Hu @ BCH

import timeit
import re
from itertools import zip_longest
from guppy import hpy


### reference: pRESTO https://bitbucket.org/kleinstein/presto/src/master/bin/CollapseSeq.py
class DuplicateSet:
    """
    A class defining unique sequence sets

    Attributes:
      seq : SeqRecord.
      missing : missing character count of SeqRecord.
      keys : list of sequence identifier.
      count : duplicate count.
    """

    # Instantiation
    def __init__(self, seq, key, missing):
        self.seq = seq
        self.missing = missing
        self.keys = [key]
        self.count = 1

    # Set length evaluation to number of duplicates
    def __len__(self):
        return len(self.keys)


def findUniqueSeq(uniq_dict, search_keys, seq_dict, max_missing=3,
                  inner=False):
    """
    Finds unique sequences

    Arguments:
      uniq_dict : a dictionary of unique sequences generated by findUniqueSeq().
      search_keys : a list containing the subset of dictionary keys to be checked.
      seq_dict : a SeqRecords dictionary generated by SeqIO.index().
      max_missing : the number of missing characters to allow in a unique sequences.
      inner : if True exclude consecutive outer ambiguous characters from iterations and matching.

    Returns:
      tuple: (uniq_dict, search_keys, dup_keys) modified from passed values.
    """

    ### reference: pRESTO https://bitbucket.org/kleinstein/presto/src/master/presto/Sequence.py
    def checkSeqEqual(seq1, seq2, ignore_chars=["N"]):
        """
        Determine if two sequences are equal, excluding missing positions

        Arguments:
          seq1 : SeqRecord object
          seq2 : SeqRecord object
          ignore_chars : Set of characters to ignore

        Returns:
          bool : True if the sequences are equal
        """
        equal = True
        # for a, b in zip(seq1.upper(), seq2.upper()):
        for a, b in zip_longest(seq1, seq2):
            if a != b and a not in ignore_chars and b not in ignore_chars:
                equal = False
                break

        return equal

    def findUID(uid, search_dict, score=False):
        """
        Checks if a unique identifier is already present in a unique dictionary

        Arguments:
          uid : the unique identifier key to check.
          search_dict : a dictionary to search for key matches in.
          score : if True score sequence element of the uid against each sequence in search_list.

        Returns:
          str: uid of match if found; None otherwise.
        """
        match = None
        # Check for exact matches
        if not score:
            match = uid if uid in search_dict else None
        # Check for ambiguous matches
        else:
            for key in search_dict:
                if checkSeqEqual(uid, key):
                    match = key
                    break
        # Return search boolean
        return match

    # Define local variables
    ambig_re = re.compile(r'[\.\-N]')
    score = (max_missing > 0)
    dup_keys = []
    to_remove = []

    # Iterate over search keys and update uniq_dict and dup_keys
    for idx, key in enumerate(search_keys):
        # Print progress of previous iteration
        # print(idx, result_count, 0.05, start_time=start_time, task='%i missing' % max_missing)

        # Define sequence to process
        seq_str = seq_dict[key]
        # seq_str = str(seq.seq)
        if inner:  seq_str = seq_str.strip('.-N')

        # Skip processing of ambiguous sequences over max_missing threshold
        ambig_count = len(ambig_re.findall(seq_str))
        if ambig_count > max_missing: continue

        uid = seq_str
        match = findUID(uid, uniq_dict, score)

        if match is None:
            uniq_dict[uid] = DuplicateSet(seq_str, key=key, missing=ambig_count)
        else:
            # Updated sequence, count, ambiguous character count, and count sets
            dup_key = key
            uniq_dict[match].keys.append(key)
            # Update duplicate list
            dup_keys.append(dup_key)
        # Mark seq for removal from later steps
        to_remove.append(idx)
    # Remove matched sequences from search_keys
    for j in reversed(to_remove):  del search_keys[j]

    return uniq_dict, search_keys, dup_keys


def collapseSeq(seqs, max_missing=500, inner=False, should_benchmark_memory=False):
    """
    Removes duplicate sequences

    Arguments:
      seqs : the input sequences
      max_missing : number of ambiguous characters to allow in a unique sequence.
      inner : if True exclude consecutive outer ambiguous characters from iterations and matching.
      should_benchmark_memory : benchmark memory usage or not.

    Returns:
      is_uniq_vec, time cost, [memory usage]
    """
    seq_dict = {}
    for i in range(len(seqs)):
        seq_dict[i] = seqs[i]   # the dict of input sequences, key = idx, value = sequence
    hp = None
    if should_benchmark_memory:
        hp = hpy()
    start_time = timeit.default_timer()
    # Find sequences with duplicates
    uniq_dict = {}
    # Added list typing for compatibility issue with Python 2.7.5 on OS X
    # TypeError: object of type 'dictionary-keyiterator' has no len()
    # list of seqs
    search_keys = list(seq_dict.keys())
    dup_keys = []
    for n in range(0, max_missing + 1):
        # Find unique sequences
        uniq_dict, search_keys, dup_list = findUniqueSeq(uniq_dict, search_keys, seq_dict, n, inner)

        # Update list of duplicates
        dup_keys.extend(dup_list)

        # Break if no keys to search remain
        if len(search_keys) == 0:  break
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