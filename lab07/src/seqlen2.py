#!/usr/bin/env python3
# seqlen2.py — FASTA 파일의 서열별 길이를 출력한다.
# 사용법: python3 seqlen2.py <FASTA파일>

import sys
from fasta import read_fasta
 
seqs = read_fasta(sys.argv[1])

for name in seqs :
    print(name, len(seqs[name]))

# 기존 코드
'''import sys
 
filename = sys.argv[1]
 
lengths = {}
name = None
 
with open(filename) as f:
    for line in f:
        line = line.rstrip()
        if line.startswith(">"):
            name = line[1:].split()[0]
            lengths[name] = 0
        else:
            lengths[name] = lengths[name] + len(line)
 
for name in lengths:
    print(name, lengths[name])'''
    