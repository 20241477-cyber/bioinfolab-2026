# GFF3 파일에서 모든 CDS 길이의 합을 계산한다. (실험 과정 8번)
# 사용법: python3 cds_total.py <GFF3 파일>
#   (parse_gff.py를 불러오므로 lab13/src 폴더 안에서 실행한다)
#   예: cd lab13/src && python3 cds_total.py ../doc/prokka_out/sample.gff
import sys
from parse_gff import read_gff

# 인자가 없으면 사용법을 알려 주고 끝낸다
if len(sys.argv) < 2:
    print("사용법: python3 cds_total.py <GFF3 파일>")
    sys.exit(1)

# 1. GFF3 파일을 읽는다
features = read_gff(sys.argv[1])

# 2. type이 CDS인 주석만 골라 개수와 길이 합을 구한다
cds_count = 0
total_length = 0
for f in features:
    if f["type"] == "CDS":
        length = f["end"] - f["start"] + 1   # CDS 하나의 길이
        cds_count = cds_count + 1
        total_length = total_length + length

# 3. 결과를 출력한다
print("CDS 총개수:", cds_count)
print("CDS 길이 총합(bp):", total_length)
