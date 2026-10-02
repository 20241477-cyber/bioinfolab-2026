#!/usr/bin/bash
# shortlines.sh - FASTA 파일의 서열 중 특정 길이보다 짧은 서열의 개수 출력
# 사용법: shortlines.sh <FASTA파일> <최소길이>

if [ -z "$1" ] 
then
    echo "사용법: $0 <FASTA파일> <최소길이>"
    echo "주어진 FASTA 파일의 서열 중 특정 길이보다 짧은 서열의 개수를 출력합니다."
    echo "오류 : FASTA 파일과 최소길이를 입력해야 합니다."
    exit 1
fi

if [ -z "$2" ]
then
    echo "사용법: $0 <FASTA파일> <최소길이>"
    echo "주어진 FASTA 파일의 서열 중 특정 길이보다 짧은 서열의 개수를 출력합니다."
    echo "오류 : 최소길이를 입력해야 합니다."
    exit 1
fi

if [ ! -f "$1" ]
then
    echo ""$1"파일이 존재하지 않습니다."
    exit 1
fi

if ! echo "$2" | awk '{if ($0 !~ /^[0-9]+$/) exit 1}'; then
    echo "오류: 두 번째 인자는 숫자여야 합니다."
    exit 1
fi

awk -v min="$2" -v file="$1" '
    BEGIN {
        count=0
    }

    $0 !~ /^>/ {
        if (length($0) < min)
            count++
    }

    END {
        print file " 파일 안 " min "개 미만의 서열 개수는 " count "개입니다."
    }
' "$1"
