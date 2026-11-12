# FASTQ 파일의 모든 read에서 위치(1번째 염기, 2번째 염기, ...)별 평균 Phred 품질 점수를 구한다.
# 사용법: python3 src/qual_by_position.py <FASTQ 파일>
import sys

def read_fastq(filename):
    records = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))
    return records

reads = read_fastq(sys.argv[1])

# totals[i]: i번째 위치(0부터 셈)의 품질 점수 합계
# counts[i]: i번째 위치에 염기가 있는 read의 개수
totals = []
counts = []

for name, seq, qual in reads:             # 바깥 반복문: read 하나씩
    for i in range(len(qual)):            # 안쪽 반복문: 그 read의 위치 하나씩
        score = ord(qual[i]) - 33         # Phred+33 변환
        if i >= len(totals):              # 처음 만나는 위치이면 칸을 하나 늘린다
            totals.append(0)
            counts.append(0)
        totals[i] = totals[i] + score
        counts[i] = counts[i] + 1

for i in range(len(totals)):
    average = totals[i] / counts[i]
    print(str(i + 1) + "\t" + str(round(average, 2)))
