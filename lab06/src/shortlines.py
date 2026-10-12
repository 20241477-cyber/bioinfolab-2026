#!/usr/bin/python3
# shortlines.py - FASTA 파일의 서열 중 특정 길이보다 짧은 서열의 개수 출력
# 사용법: shortlines.py <FASTA파일> <최소길이>

import os
import sys

if len(sys.argv) < 2 :
    print("사용법: shortlines.py <FASTA파일> <최소길이>")
    print("주어진 FASTA 파일의 서열 중 특정 길이보다 짧은 서열의 개수를 출력합니다.")
    print("오류 : FASTA 파일과 최소길이를 입력해야 합니다.")
    sys.exit(1)

if len(sys.argv) < 3 :
    print("사용법: shortlines.py <FASTA파일> <최소길이>")
    print("주어진 FASTA 파일의 서열 중 특정 길이보다 짧은 서열의 개수를 출력합니다.")
    print("오류 : 최소길이를 입력해야 합니다.")
    sys.exit(1)

if not os.path.isfile(sys.argv[1]):
    print(sys.argv[1] + "파일이 존재하지 않습니다.")
    sys.exit(1)

if not sys.argv[2].isdigit():
    print("오류: 두 번째 인자는 숫자여야 합니다.")
    sys.exit(1)

min_length = int(sys.argv[2])
file_name = sys.argv[1]

count = 0

with open(file_name) as f:
    for line in f:
        line = line.rstrip()
        if line.startswith('>'):
            count = count + 0
        else:
            if len(line) < min_length:
                 count = count + 1
            else :
                 count = count + 0
                
print(file_name, " 파일 안", min_length, "개 미만의 서열 개수는", count, "개입니다.")
