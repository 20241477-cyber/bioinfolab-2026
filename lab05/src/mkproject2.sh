#!/usr/bin/bash
# mkproject2.sh - 프로젝트 폴더와 기본 파일을 생성한다

#조건 적용
if [ -z "$1" ]
then
    echo "사용법: $0 <프로젝트 폴더 이름>"
    echo " 주어진 폴더이름의 폴더를 생성합니다."
    exit 1
fi

if [ -d "$1" ]
then
    echo "오류: 폴더가 이미 존재합니다 : $1"
    exit 1
fi

# 폴더 생성
NAME="$1"
mkdir "$NAME"
echo "$NAME 폴더를 만들었습니다"
