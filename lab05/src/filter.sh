#!/usr/bin/bash
# filter.sh — FASTA 파일을 필터링하여 조건에 맞는 서열의 이름을 출력한다
# 사용법: filter.sh <FASTA파일>
# claude 이용

file=$1

name=""
seq=""
length=0
gc=0
n=0

while read line
do
    if [[ "$line" == ">"* ]]
    then
        if [ -n "$name" ]
        then
            length=${#seq}
            gc_count=$(echo "$seq" | grep -o "[GC]" | wc -l)
            n=$(echo "$seq" | grep -o "N" | wc -l)

            if [ "$length" -ge 500 ] && [ "$length" -le 3000 ]
            then
                if [ "$gc_count" -ge 200 ]
                then
                    if [[ "$name" != *badword* ]]
                    then
                        if [ "$n" -lt 5 ]
                        then
                            echo "$name"
                        fi
                    fi
                fi
            fi
        fi

        name="${line#>}"
        seq=""
    else
        seq="$seq$line"
    fi

done < "$file"

# 마지막 서열 처리
if [ -n "$name" ]
then
    length=${#seq}
    gc_count=$(echo "$seq" | grep -o "[GC]" | wc -l)
    n=$(echo "$seq" | grep -o "N" | wc -l)

    if [ "$length" -ge 500 ] && [ "$length" -le 3000 ]
    then
        if [ "$gc_count" -ge 200 ]
        then
            if [[ "$name" != *badword* ]]
            then
                if [ "$n" -lt 5 ]
                then
                    echo "$name"
                fi
            fi
        fi
    fi
fi