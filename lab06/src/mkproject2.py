#!/usr/bin/python3
# mkproject2.py - 프로젝트 폴더와 기본 파일을 생성한다
import os
import sys

#조건 적용
if len(sys.argv) < 2 :
    print("사용법: src/mkproject2.py <프로젝트 폴더 이름>")
    print("주어진 폴더이름의 폴더를 생성합니다.")
    sys.exit(1)

foldername = sys.argv[1]

if os.path.isdir(foldername) :
    print("오류: 폴더가 이미 존재합니다 : ", foldername)
    sys.exit(1)

# 폴더 생성
os.makedirs(foldername + "/data")
os.makedirs(foldername + "/doc")
os.makedirs(foldername + "/src")
print(foldername, "폴더와 하위폴더들을 만들었습니다")
