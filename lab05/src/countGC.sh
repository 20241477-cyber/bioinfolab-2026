#!/usr/bin/bash
# 서열의 GC비율을 소수점 넷째자리까지 출력하는 스크립트
# : bc 활용

SEQ="ATGCGATACGCTTGA"
LEN=${#SEQ}
GC=$(echo "$SEQ" | grep -o "[GC]" | wc -l)

echo "scale=4; $GC / $LEN" | bc