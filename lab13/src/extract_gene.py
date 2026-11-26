# 목적: Prokka GFF3 주석에서 유전자(CDS 또는 tRNA)를 찾아
#       contigs.fa에서 그 염기서열을 잘라 FASTA 형식으로 출력한다.
#       (sample.ffn과의 비교는 이 스크립트에서 하지 않고 따로 진행한다)
# 사용법: python3 src/extract_gene.py <GFF3 파일> <contigs.fa> <유전자 이름 또는 ID>
# 예시:   python3 src/extract_gene.py doc/prokka_out/sample.gff data/contigs.fa deoB
#         python3 src/extract_gene.py doc/prokka_out/sample.gff data/contigs.fa deoB > doc/deoB.fasta
# 출력: 표준 출력(stdout)에는 FASTA 헤더와 염기서열만 출력한다.
#       유전자 정보, 안내, 오류 메시지는 모두 표준 오류(stderr)로 출력한다.
# 주의: parse_gff.py는 import될 때 sys.argv[1]을 GFF 파일로 읽어 "주석 개수"를 출력한다.
#       그래서 GFF3 파일을 반드시 첫 번째 인자로 넣어야 한다.

import sys
import os

# 인자 개수 확인 (parse_gff를 import하기 전에 확인해야 한다)
if len(sys.argv) < 4:
    print("사용법: python3 extract_gene.py <GFF3 파일> <contigs.fa> <유전자 이름 또는 ID>", file=sys.stderr)
    sys.exit(1)

# 같은 폴더(lab13/src)의 parse_gff.py에서 read_gff() 함수를 가져온다
# parse_gff.py는 import될 때 "주석 개수"를 print()로 출력하는데,
# 그대로 두면 FASTA 결과에 섞이므로 import하는 동안만 출력을 stderr로 보낸다
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


def get_attributes(text):
    """'ID=a;Name=b;...' 형태의 문자열을 {키: 값} 딕셔너리로 바꾼다."""
    attrs = {}
    for item in text.split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            attrs[key] = value
    return attrs


def reverse_complement(seq):
    """서열의 역상보 서열을 돌려준다. A/C/G/T 이외의 글자는 N으로 바꾼다."""
    complement = {"A": "T", "T": "A", "G": "C", "C": "G"}
    result = ""
    for base in seq.upper():
        if base in complement:
            result = complement[base] + result   # 앞에 붙이면 뒤집기도 함께 된다
        else:
            result = "N" + result
    return result


# ----- 1. 인자 받기 -----
gff_file = sys.argv[1]
contig_file = sys.argv[2]
query = sys.argv[3]

# 검색할 attributes 키 목록
search_keys = ["ID", "Name", "gene", "locus_tag"]

# ----- 2. GFF3에서 유전자 찾기 -----
features = read_gff(gff_file)

found = []        # 정확히 일치하는 유전자
candidates = []   # 비슷한 이름 (예: phnE -> phnE_1, phnE_2)

for feature in features:
    # CDS와 tRNA만 대상으로 한다
    if feature["type"] != "CDS" and feature["type"] != "tRNA":
        continue

    attrs = get_attributes(feature["attributes"])
    matched = False
    similar = False
    for key in search_keys:
        if key in attrs:
            if attrs[key] == query:
                matched = True
            elif attrs[key].startswith(query + "_"):
                similar = True

    # ID와 locus_tag가 같아도 한 유전자는 한 번만 넣는다
    if matched:
        found.append(feature)
    elif similar:
        candidates.append(feature)

# ----- 3. 검색 결과가 0개 또는 여러 개인 경우 안내 (stderr) -----
if len(found) == 0:
    print("[안내] '" + query + "'와 정확히 일치하는 CDS/tRNA 유전자가 없습니다.", file=sys.stderr)
    print("       (검색한 항목: " + ", ".join(search_keys) + ")", file=sys.stderr)
    if len(candidates) > 0:
        print("       이름이 비슷한 유전자가 " + str(len(candidates)) + "개 있습니다. 아래 ID 중 하나로 다시 실행하세요.", file=sys.stderr)
        for feature in candidates:
            attrs = get_attributes(feature["attributes"])
            print("       " + attrs["ID"] + "\t" + attrs.get("Name", "-") + "\t" + feature["type"], file=sys.stderr)
    sys.exit(1)

if len(found) > 1:
    print("[안내] '" + query + "'로 검색된 유전자가 " + str(len(found)) + "개입니다. 아래 ID 중 하나로 다시 실행하세요.", file=sys.stderr)
    for feature in found:
        attrs = get_attributes(feature["attributes"])
        print("       " + attrs["ID"] + "\t" + attrs.get("Name", "-") + "\t" + feature["type"]
              + "\t" + feature["seqid"] + ":" + str(feature["start"]) + "-" + str(feature["end"])
              + "(" + feature["strand"] + ")", file=sys.stderr)
    sys.exit(1)

# ----- 4. 유전자 정보 꺼내기 (stderr) -----
gene = found[0]
attrs = get_attributes(gene["attributes"])
gene_id = attrs["ID"]
gene_type = gene["type"]
seqid = gene["seqid"]
start = gene["start"]
end = gene["end"]
strand = gene["strand"]

print("[유전자 정보]", file=sys.stderr)
print("  ID      :", gene_id, file=sys.stderr)
print("  이름    :", attrs.get("Name", "-"), file=sys.stderr)
print("  종류    :", gene_type, file=sys.stderr)
print("  product :", attrs.get("product", "-"), file=sys.stderr)
print("  위치    :", seqid, start, end, strand, file=sys.stderr)

# ----- 5. contigs.fa에서 서열 잘라내기 -----
contigs = read_fasta(contig_file)
if seqid not in contigs:
    print("[오류] contigs 파일에 " + seqid + " 서열이 없습니다.", file=sys.stderr)
    sys.exit(1)

# GFF3: 1부터 시작, 끝 포함  ->  Python: 0부터 시작, 끝 미포함
# 따라서 시작은 1을 빼고, 끝은 그대로 쓴다
seq = contigs[seqid][start - 1:end].upper()

# ----- 6. 역방향(-) 유전자는 역상보 서열로 바꾸기 -----
if strand == "-":
    seq = reverse_complement(seq)

print("  길이    :", len(seq), "bp (GFF3 계산값:", end - start + 1, "bp)", file=sys.stderr)

# ----- 7. FASTA 형식으로 출력 (stdout, 60글자마다 줄바꿈) -----
# 표준 출력에는 FASTA 헤더와 서열만 출력한다
print(">" + gene_id + " " + gene_type + " " + seqid + ":" + str(start) + "-" + str(end) + "(" + strand + ")")
for i in range(0, len(seq), 60):
    print(seq[i:i + 60])
