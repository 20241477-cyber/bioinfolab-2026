#!/usr/bin/bash
# countseq.sh — FASTA 파일의 서열 개수를 출력한다
# 사용법: countseq.sh <FASTA파일>
# claude 이용

file=$1

name=""
length=0

while read line
do
    if [[ "$line" == ">"* ]]
    then
        if [ -n "$name" ]
        then
            echo "$name $length"
        fi

        name="${line#>}"
        length=0
    else
        length=$((length + ${#line}))
    fi
done < "$file"

if [ -n "$name" ]
then
    echo "$name $length"
fi