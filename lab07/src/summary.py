#!/usr/bin/env python3
# summary.py — FASTA 파일의 서열별 이름, 길이, GC비율을 TSV로 저장한다.
# 사용법: python3 summary.py <FASTA파일> <저장할 파일 이름>

import sys
from fasta import read_fasta, gc_content
 
infile = sys.argv[1]
outfile = sys.argv[2]

seqs = read_fasta(infile)
 
with open(outfile, "w") as out:
    out.write("name\tlength\tgc\n")
    for name in seqs:
        seq = seqs[name]
        gc = round(gc_content(seq), 4)
        out.write(name + "\t" + str(len(seq)) + "\t" + str(gc) + "\n")
 
print(len(seqs), "개 서열을", outfile, "에 저장했습니다.")
