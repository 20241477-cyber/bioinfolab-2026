#!/usr/bin/env python3
# count_agent.py — FASTA 파일의 서열 개수를 출력한다
# 사용법: python3 src/count_agent.py <FASTA파일>

import sys
import os

if len(sys.argv) < 2:
    print("사용법: python3 count_agent.py <FASTA파일>")
    sys.exit(1)

filename = sys.argv[1]

if not os.path.isfile(filename):
    print("오류: 파일을 찾을 수 없습니다:", filename)
    sys.exit(2)

# '>'로 시작하는 헤더 줄 하나가 서열 하나다
count = 0
with open(filename) as f:
    for line in f:
        if line.startswith(">"):
            count = count + 1

print(count)
