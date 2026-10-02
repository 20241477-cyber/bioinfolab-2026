#!/usr/bin/bash
# batchinfo2.sh 
# :폴더 안의 FASTA 파일별 서열 개수 출력
#   및 원하는 파일의 서열 개수를 출력하는 스크립트
# 사용법: batchinfo2.sh <폴더> <FASTA 파일명>

#조건 설정
if [  -z "$1" ]
then
    echo "사용법: $0 <폴더명> <FASTA 파일명>"
    echo "주어진 폴더 안의 FASTA 파일별 서열 개수 출력합니다."
    echo "원하는 파일의 서열 개수를 출력합니다." 
    exit 1
fi

if [ ! -d "$1" ]
then
    echo "오류: 폴더를 찾을 수 없습니다: $1"
    exit 1
fi

found=0
for F in "$1"/*.fasta
do
    if [ -f "$F" ]
    then
        found=1
        break
    fi
done

if [ "$found" -eq 0 ]
then
    echo ""$1" 폴더에 fasta 파일이 없습니다."
    exit 1
fi

if [ ! -f "$1/$2" ] 
then 
    echo ""$2"파일이 "$1"폴더 안에 없습니다." 
    exit 1 
fi 

# 첫번째 행 출력(열 제목)
DIR="$1"
echo "file      count" > doc/batchinfo2.txt

# 서열 이름 및 개수 출력
for F in "$DIR"/*.fasta
do
    N=$(grep -c ">" "$F")
    echo "$F    $N"  >> doc/batchinfo2.txt
done

# 원하는 FASTA 파일의 서열 개수
N2=$(grep "$2" doc/batchinfo2.txt) #지정 FASTA 파일명과 서열 개수
echo "지정 파일 이름      파일의 서열 개수"
echo "$N2"