#!/usr/bin/bash
# fastainfo.sh - FASTA 파일의 요약 정보를 출력한다.
# 사용법: fastainfo.sh <FASTA파일>

# 조건 확인
if [ -z "$1" ]
then
    echo "사용법: $0 <FASTA파일>"
    echo "  주어진 FASTA 파일의 서열 개수를 출력합니다."
    exit 1
fi
 
if [ ! -f "$1" ]
then
    echo "오류: 파일을 찾을 수 없습니다: $1"
    exit 1
fi


# 파일명 출력
FILE=$1
echo "파일: $FILE"

# 서열 개수 출력
N=$(grep -c ">" "$FILE")
echo "서열 개수: $N"

# 서열 이름 출력
echo "서열 이름:"
grep ">" "$FILE" | cut -d " " -f1 | tr -d ">"

# 총 염기 수 출력
LEN=$(grep -v ">" "$FILE" | tr -d "\n" | wc -c)
echo "총 염기 수(대략): $LEN"