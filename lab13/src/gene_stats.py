# GFF3 파일에서 CDS의 길이와 방향(strand)을 분석한다.
# 사용법: python3 gene_stats.py <GFF3 파일>
#   (parse_gff.py를 불러오므로 lab13/src 폴더 안에서 실행한다)
#   예: cd lab13/src && python3 gene_stats.py ../doc/prokka_out/sample.gff
import sys
from parse_gff import read_gff

# 1. GFF3 파일을 읽고 type이 CDS인 주석만 고른다
features = read_gff(sys.argv[1])

cds_list = []
for f in features:
    if f["type"] == "CDS":
        cds_list.append(f)

if len(cds_list) == 0:
    print("CDS 주석이 없습니다.")
    sys.exit(1)

# 2. 각 CDS의 길이를 end - start + 1로 계산해 저장한다
for cds in cds_list:
    cds["length"] = cds["end"] - cds["start"] + 1

# 3. 총개수, 평균, 최소, 최대 길이를 구한다
total = 0
min_len = cds_list[0]["length"]
max_len = cds_list[0]["length"]
for cds in cds_list:
    total = total + cds["length"]
    if cds["length"] < min_len:
        min_len = cds["length"]
    if cds["length"] > max_len:
        max_len = cds["length"]
average = total / len(cds_list)

# 4. 정방향(+)과 역방향(-) CDS의 개수를 센다
plus_count = 0
minus_count = 0
for cds in cds_list:
    if cds["strand"] == "+":
        plus_count = plus_count + 1
    elif cds["strand"] == "-":
        minus_count = minus_count + 1

# 결과 출력: 길이 통계와 방향
print()
print("=== CDS 길이 통계 ===")
print("CDS 총개수:", len(cds_list))
print("평균 길이:", round(average, 1), "bp")
print("최소 길이:", min_len, "bp")
print("최대 길이:", max_len, "bp")
# 6. 평균 길이를 3으로 나누면 평균 단백질 길이(코돈 수)에 해당한다
print("평균 길이 / 3:", round(average / 3, 1), "(아미노산 수에 해당)")

print()
print("=== CDS 방향 ===")
print("정방향(+):", plus_count, "개")
print("역방향(-):", minus_count, "개")

# 5. 길이 기준 내림차순으로 정렬하고 가장 긴 CDS 5개를 출력한다
def get_length(cds):
    return cds["length"]

sorted_cds = sorted(cds_list, key=get_length, reverse=True)

print()
print("=== 가장 긴 CDS 5개 ===")
print("순위", "contig", "시작", "끝", "길이(bp)", "strand", "attributes", sep="\t")
rank = 1
for cds in sorted_cds[:5]:
    print(rank, cds["seqid"], cds["start"], cds["end"], cds["length"],
          cds["strand"], cds["attributes"], sep="\t")
    rank = rank + 1
    