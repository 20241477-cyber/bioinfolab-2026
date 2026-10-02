#!/usr/bin/bash
# batchinfo.sh - 폴더 안의 FASTA 파일 별 서열 개수를 출력한다
# 사용법: batchinfo.sh <폴더>

#조건 설정
if [ ! -d "$1" ]
then
    echo "오류: 폴더를 찾을 수 없습니다: $1"
    exit 1
fi

if [ ! -f "$1"/*.fasta ]
then
    echo ""$1"폴더에 fasta 파일이 없습니다."
    exit 1
fi

# 첫번째 행 출력(열 제목)
DIR="$1"
echo "file      count"

# 서열 이름 및 개수 출력
for F in "$DIR"/*.fasta
do
    N=$(grep -c ">" "$F")
    echo "$F    $N"
done