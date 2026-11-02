#!/usr/bin/env python3
# count_agent3.py — FASTA 파일의 서열 개수를 출력한다 (PYTHONPATH로 lab07의 read_fasta 사용)
# 사용법: PYTHONPATH=lab07/src python3 lab09/src/count_agent3.py <FASTA파일>   # 저장소 루트에서 실행
#
# fasta.py의 위치를 코드 안에 적지 않고, 실행할 때 PYTHONPATH 환경 변수로 알려 준다.

import sys
import os

from fasta import read_fasta

if len(sys.argv) < 2:
    print("사용법: PYTHONPATH=lab07/src python3 count_agent3.py <FASTA파일>")
    sys.exit(1)

filename = sys.argv[1]

if not os.path.isfile(filename):
    print("오류: 파일을 찾을 수 없습니다:", filename)
    sys.exit(2)

# read_fasta()는 {이름: 서열} 딕셔너리를 돌려주므로 항목 수가 서열 개수다
seqs = read_fasta(filename)
print(len(seqs))
