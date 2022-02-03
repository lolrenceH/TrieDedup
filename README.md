# TrieDedup


High-throughput sequencing is powerful and extensively applied in biological studies, although sequencers may report bases with low qualities and lead to ambiguous bases, 'N's. PCR duplicates introduced in library preparation need to be removed in genomics studies, and many deduplication tools have been developed for this purpose. However, the existing tools cannot deal with 'N's correctly or efficiently. Here we proposed and implemented TrieDedup, which uses trie (prefix tree) structure to compare and store sequences. TrieDedup can handle ambiguous base 'N's, and efficiently deduplicate at the level of raw sequences. We also reduced its memory usage by implementing restrictedListDict. We benchmarked the performance, and showed that TrieDedup can deduplicate reads up to 160X faster speed than pairwise comparison, with 36X higher memory usage.


Author : Jianqiao Hu & Adam Yongxin Ye @ BCH
