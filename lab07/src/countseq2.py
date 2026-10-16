#!/usr/bin/env python3
# countseq2.py — FASTA 파일의 서열 개수를 출력한다
# 사용법: python3 src/countseq2.py <FASTA파일>

import sys
import os
from fasta import read_fasta

if len(sys.argv) < 2:
    print("사용법: python3 countseq.py <FASTA파일>")
    sys.exit(1)

filename = sys.argv[1]

if not os.path.isfile(filename):
    print("오류: 파일을 찾을 수 없습니다:", filename)
    sys.exit(2)
from fasta import read_fasta
 
seqs = read_fasta(sys.argv[1])
print(len(seqs))

