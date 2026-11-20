# 주어진 contig 길이 목록으로 N50을 계산하는 연습용 스크립트
# (lab12/src/n50.py의 N50 계산 방식을 그대로 따른다)
# 사용법: python3 src/n50_test.py

def n50(lengths):
    # 1. contig 길이를 큰 것부터 작은 것 순서(내림차순)로 정렬한다
    lengths = sorted(lengths, reverse=True)
    # 2. 전체 길이와 그 절반을 구한다
    total = sum(lengths)
    half = total / 2

    # 3. 긴 contig부터 길이를 더해 가다가
    #    누적 길이가 절반 이상이 되는 순간의 contig 길이가 N50이다
    running = 0
    for length in lengths:
        running = running + length
        print("  contig 길이", length, "-> 누적 길이", running)
        if running >= half:
            return length

contigs = [12, 3, 20, 8, 1, 15, 6]

print("contig 길이:", contigs)
print("정렬 결과(내림차순):", sorted(contigs, reverse=True))
print("전체 길이:", sum(contigs))
print("전체 길이의 절반:", sum(contigs) / 2)
print("누적 과정:")
result = n50(contigs)
print("N50:", result)
