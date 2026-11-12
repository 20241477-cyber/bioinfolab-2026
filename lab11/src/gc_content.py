# FASTQ 파일의 모든 read에서 GC 함량을 계산하고,
# GC 함량이 가장 높은 read와 가장 낮은 read의 이름, GC 함량(%), 평균 품질을 출력한다.
# 전체 read의 평균 품질도 함께 출력하여 두 read와 비교할 수 있게 한다.
# 또 GC 함량 상위 10개, 하위 10개 read를 출력하고 각 그룹의 평균 품질을 전체 평균과 비교한다.
# GC 함량이 같은 read가 여러 개이면 파일에서 처음 나온 read를 선택(우선)한다.
# 사용법: python3 src/gc_content.py <FASTQ 파일>
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

def gc_content(seq):
    # (G 개수 + C 개수) / 서열 길이 x 100
    gc = 0
    for base in seq:
        if base == "G" or base == "C":
            gc = gc + 1
    return gc / len(seq) * 100

def mean_quality(qual):
    # qual_summary.py와 같은 방법: Phred+33 점수의 평균
    scores = []
    for ch in qual:
        scores.append(ord(ch) - 33)
    return sum(scores) / len(scores)

def get_gc(record):
    # 정렬할 때 기준으로 쓸 값: (이름, GC 함량, 평균 품질) 중 GC 함량
    return record[1]

def print_group(title, group):
    # read 묶음을 순위, 이름, GC 함량, 평균 품질 순서로 출력하고 그룹 평균 품질을 돌려준다
    print(title)
    print("순위\t이름\tGC 함량(%)\t평균 품질")
    group_total = 0
    rank = 1
    for name, gc, q in group:
        print(str(rank) + "\t" + name + "\t" + str(round(gc, 2)) + "\t" + str(round(q, 2)))
        group_total = group_total + q
        rank = rank + 1
    return group_total / len(group)

reads = read_fastq(sys.argv[1])

# 가장 높은 read와 가장 낮은 read의 정보를 담을 변수
max_name = ""
max_gc = -1        # 어떤 GC 함량(0 이상)보다도 작은 값으로 시작
max_q = 0
min_name = ""
min_gc = 101       # 어떤 GC 함량(100 이하)보다도 큰 값으로 시작
min_q = 0

total_q = 0        # read별 평균 품질의 합계
results = []       # 모든 read의 (이름, GC 함량, 평균 품질)을 파일 순서대로 모은다

for name, seq, qual in reads:
    gc = gc_content(seq)
    q = mean_quality(qual)
    total_q = total_q + q
    results.append((name, gc, q))

    # '>'와 '<'를 쓰므로 값이 같을 때는 바꾸지 않는다 → 처음 발견한 read가 남는다
    if gc > max_gc:
        max_name = name
        max_gc = gc
        max_q = q
    if gc < min_gc:
        min_name = name
        min_gc = gc
        min_q = q

all_q = total_q / len(reads)

# 상위 10개 / 하위 10개 고르기
# sorted()는 GC 함량이 같은 read끼리는 원래 순서(파일 순서)를 그대로 유지한다.
# reverse=True(큰 값부터)로 정렬해도 같은 값끼리의 순서는 유지되므로,
# 동점이면 파일에서 먼저 나온 read가 앞에 온다.
high_sorted = sorted(results, key=get_gc, reverse=True)   # GC 높은 순
low_sorted = sorted(results, key=get_gc)                  # GC 낮은 순
top10 = high_sorted[0:10]
bottom10 = low_sorted[0:10]

print("분석한 read 개수: " + str(len(reads)))
print()
print("[GC 함량이 가장 높은 read]")
print("이름: " + max_name)
print("GC 함량(%): " + str(round(max_gc, 2)))
print("평균 품질: " + str(round(max_q, 2)))
print()
print("[GC 함량이 가장 낮은 read]")
print("이름: " + min_name)
print("GC 함량(%): " + str(round(min_gc, 2)))
print("평균 품질: " + str(round(min_q, 2)))
print()
print("[품질 비교]")
print("전체 read 평균 품질: " + str(round(all_q, 2)))
print("GC 최고 read - 전체 평균: " + str(round(max_q - all_q, 2)))
print("GC 최저 read - 전체 평균: " + str(round(min_q - all_q, 2)))
print()
top_q = print_group("[GC 함량 상위 10개 read]", top10)
print()
bottom_q = print_group("[GC 함량 하위 10개 read]", bottom10)
print()
print("[그룹별 품질 비교]")
print("상위 10개 그룹 평균 품질: " + str(round(top_q, 2)))
print("하위 10개 그룹 평균 품질: " + str(round(bottom_q, 2)))
print("전체 read 평균 품질: " + str(round(all_q, 2)))
print("상위 10개 그룹 - 전체 평균: " + str(round(top_q - all_q, 2)))
print("하위 10개 그룹 - 전체 평균: " + str(round(bottom_q - all_q, 2)))
