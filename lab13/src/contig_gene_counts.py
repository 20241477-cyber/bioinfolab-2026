# 목적: Prokka GFF3 주석에서 contig별로 CDS와 tRNA 개수를 세고,
#       contigs.fa에서 구한 contig 길이와 함께 표로 출력한다. (실험 문제 4번)
#       유전자가 하나도 없는 contig도 포함하며, contig 길이가 긴 순서로 정렬한다.
# 사용법: python3 src/contig_gene_counts.py <GFF3 파일> <contigs.fa>
# 예시:   python3 src/contig_gene_counts.py doc/prokka_out/sample.gff data/contigs.fa
# 주의: parse_gff.py는 import될 때 sys.argv[1]을 GFF 파일로 읽어 "주석 개수"를 출력한다.
#       그래서 GFF3 파일을 반드시 첫 번째 인자로 넣어야 한다.

import sys
import os

# 인자 개수 확인 (parse_gff를 import하기 전에 확인해야 한다)
if len(sys.argv) < 3:
    print("사용법: python3 contig_gene_counts.py <GFF3 파일> <contigs.fa>", file=sys.stderr)
    sys.exit(1)

gff_file = sys.argv[1]
fasta_file = sys.argv[2]

# 같은 폴더(lab13/src)의 parse_gff.py에서 read_gff() 함수를 가져온다
# parse_gff.py는 import될 때 "주석 개수"를 print()로 출력하는데,
# 표 결과에 섞이지 않도록 import하는 동안만 출력을 stderr로 보낸다
original_stdout = sys.stdout
sys.stdout = sys.stderr
from parse_gff import read_gff
sys.stdout = original_stdout

# lab07/src/fasta.py의 read_fasta() 함수를 가져온다
# 이 파일 위치(lab13/src)에서 두 단계 위로 올라가 lab07/src 폴더를 찾는다
this_folder = os.path.dirname(os.path.abspath(__file__))
lab07_src = os.path.join(this_folder, "..", "..", "lab07", "src")
sys.path.append(lab07_src)
from fasta import read_fasta


# 1. contigs.fa를 읽어 각 contig의 길이를 구한다
#    read_fasta()는 헤더의 첫 단어(예: contig00001)를 이름으로 쓴다
seqs = read_fasta(fasta_file)

lengths = {}     # {contig 이름: 길이(bp)}
cds_count = {}   # {contig 이름: CDS 개수}
trna_count = {}  # {contig 이름: tRNA 개수}

# 모든 contig를 0개로 먼저 등록해 두면 유전자가 없는 contig도 결과에 남는다
for name in seqs:
    lengths[name] = len(seqs[name])
    cds_count[name] = 0
    trna_count[name] = 0

# 2. GFF3를 읽어 첫 번째 열(seqid)을 기준으로 CDS와 tRNA 개수를 센다
features = read_gff(gff_file)

for feature in features:
    seqid = feature["seqid"]
    ftype = feature["type"]

    # CDS와 tRNA가 아니면 건너뛴다
    if ftype != "CDS" and ftype != "tRNA":
        continue

    # FASTA에 없는 contig 이름이 GFF3에 나오면 알려 주고 건너뛴다
    if seqid not in lengths:
        print("경고: " + seqid + "는 FASTA 파일에 없습니다.", file=sys.stderr)
        continue

    if ftype == "CDS":
        cds_count[seqid] = cds_count[seqid] + 1
    else:
        trna_count[seqid] = trna_count[seqid] + 1

# 3. contig 길이가 긴 순서로 정렬한다
#    (길이, 이름) 쌍의 리스트를 만들고 reverse=True로 내림차순 정렬한다
pairs = []
for name in lengths:
    pairs.append((lengths[name], name))
pairs.sort(reverse=True)

# 4. 표를 출력한다 (열은 탭으로 구분)
print("contig\tlength_bp\tCDS\ttRNA\ttotal_genes")

total_cds = 0
total_trna = 0

for pair in pairs:
    name = pair[1]
    length = pair[0]
    cds = cds_count[name]
    trna = trna_count[name]
    total = cds + trna

    print(name + "\t" + str(length) + "\t" + str(cds) + "\t" + str(trna) + "\t" + str(total))

    total_cds = total_cds + cds
    total_trna = total_trna + trna

# 5. 마지막에 전체 합계를 출력한다
print()
print("전체 contig 수:\t" + str(len(pairs)))
print("CDS 총개수:\t" + str(total_cds))
print("tRNA 총개수:\t" + str(total_trna))
print("전체 유전자 개수:\t" + str(total_cds + total_trna))
