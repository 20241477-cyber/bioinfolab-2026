# 트리밍 전 FASTQ 파일과 트리밍 후 FASTQ 파일을 읽어 다섯 가지 항목을 계산하고 나란히 비교한다.
# 항목: 전체 read 개수, 평균 read 길이, 전체 평균 Phred 품질 점수, 가장 짧은 read 길이, 가장 긴 read 길이
# 전체 평균 품질은 qual_summary.py와 같은 방법(read별 평균 품질을 구한 뒤 다시 평균)으로 계산한다.
# 사용법: python3 src/compare_fastq.py <트리밍 전 FASTQ> <트리밍 후 FASTQ>
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

def mean_quality(qual):
    # qual_summary.py와 같은 방법: Phred+33 점수의 평균
    scores = []
    for ch in qual:
        scores.append(ord(ch) - 33)
    return sum(scores) / len(scores)

def summarize(filename):
    # FASTQ 파일 하나에서 다섯 가지 항목을 계산하여 차례대로 돌려준다
    reads = read_fastq(filename)

    lengths = []      # read마다의 길이
    qualities = []    # read마다의 평균 품질
    for name, seq, qual in reads:
        lengths.append(len(seq))
        qualities.append(mean_quality(qual))

    count = len(reads)
    mean_length = sum(lengths) / count
    mean_qual = sum(qualities) / count     # read별 평균 품질의 평균
    min_length = min(lengths)
    max_length = max(lengths)
    return count, mean_length, mean_qual, min_length, max_length

before_file = sys.argv[1]
after_file = sys.argv[2]

before = summarize(before_file)
after = summarize(after_file)

labels = ["전체 read 개수", "평균 read 길이", "전체 평균 품질", "최소 read 길이", "최대 read 길이"]

print("트리밍 전: " + before_file)
print("트리밍 후: " + after_file)
print()
print("항목\t트리밍 전\t트리밍 후\t차이(후-전)")
for i in range(len(labels)):
    b = before[i]
    a = after[i]
    print(labels[i] + "\t" + str(round(b, 2)) + "\t" + str(round(a, 2)) + "\t" + str(round(a - b, 2)))
