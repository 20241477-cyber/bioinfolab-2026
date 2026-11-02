#!/usr/bin/env python3
# count_agent2.py — FASTA 파일의 서열 개수를 출력한다 (lab07의 read_fasta 사용)
# 사용법: python3 src/count_agent2.py <FASTA파일>

import sys
import os

# lab07/src/fasta.py를 찾을 수 있도록 그 폴더를 모듈 검색 경로에 넣는다
# (이 스크립트 위치 기준: lab09/src -> ../../lab07/src)
here = os.path.dirname(os.path.abspath(__file__))
fasta_dir = os.path.join(here, "..", "..", "lab07", "src")
sys.path.append(fasta_dir)

from fasta import read_fasta

if len(sys.argv) < 2:
    print("사용법: python3 count_agent2.py <FASTA파일>")
    sys.exit(1)

filename = sys.argv[1]

if not os.path.isfile(filename):
    print("오류: 파일을 찾을 수 없습니다:", filename)
    sys.exit(2)

# read_fasta()는 {이름: 서열} 딕셔너리를 돌려주므로 항목 수가 서열 개수다
seqs = read_fasta(filename)
print(len(seqs))
