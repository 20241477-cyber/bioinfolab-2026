# GFF3 파일의 9번째 열(attributes)을 파싱하여 CDS의 product, gene 정보를 분석한다. (실험 문제 3번)
# 사용법: python3 analyze_attributes.py <GFF3 파일>
#   (parse_gff.py를 불러오므로 lab13/src 폴더 안에서 실행한다)
#   예: cd lab13/src && python3 analyze_attributes.py ../doc/prokka_out/sample.gff
import sys
from parse_gff import read_gff


def parse_attributes(text):
    # attributes 문자열을 딕셔너리로 바꾼다
    # 예: "ID=abc;gene=glnQ;product=..." -> {"ID": "abc", "gene": "glnQ", "product": "..."}
    attrs = {}
    for item in text.split(";"):
        # 빈 항목(끝에 ;가 붙은 경우 등)이나 =가 없는 항목은 건너뛴다
        if "=" not in item:
            continue
        # 첫 번째 = 를 기준으로 이름과 값을 나눈다
        parts = item.split("=", 1)
        name = parts[0]
        value = parts[1]
        attrs[name] = value
    return attrs


# 인자가 없으면 사용법을 알려 주고 끝낸다
if len(sys.argv) < 2:
    print("사용법: python3 analyze_attributes.py <GFF3 파일>")
    sys.exit(1)

# 1. GFF3 파일을 읽는다
features = read_gff(sys.argv[1])

# 2. CDS만 골라 attributes를 분석한다
cds_count = 0           # 전체 CDS 개수
product_count = 0       # product 정보가 있는 CDS 개수
hypo_count = 0          # product가 정확히 "hypothetical protein"인 CDS 개수
gene_count = 0          # gene 키가 있는 CDS 개수 (Name 키와는 구분한다)

for f in features:
    if f["type"] != "CDS":
        continue

    cds_count = cds_count + 1
    attrs = parse_attributes(f["attributes"])

    if "product" in attrs:
        product_count = product_count + 1
        if attrs["product"] == "hypothetical protein":
            hypo_count = hypo_count + 1

    if "gene" in attrs:
        gene_count = gene_count + 1

# 3. hypothetical protein 비율(%)을 계산한다 (CDS가 없으면 0으로 둔다)
if cds_count > 0:
    hypo_percent = hypo_count / cds_count * 100
else:
    hypo_percent = 0

# 4. 결과를 출력한다
print("전체 CDS 개수:", cds_count)
print("product 정보가 있는 CDS 개수:", product_count)
print("hypothetical protein CDS 개수:", hypo_count)
print("hypothetical protein 비율(%):", round(hypo_percent, 2))
print("gene 이름이 있는 CDS 개수:", gene_count)
