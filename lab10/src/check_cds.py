# rbcL_*.gb 파일을 Biopython으로 읽어서, CDS를 table=11로 번역한 결과가
# GenBank의 /translation 과 같은지 확인한다.
# 결과는 탭으로 구분해서 화면에 출력한다.
# 사용법: python3 src/check_cds.py data
import sys
import os
from Bio import SeqIO

folder = sys.argv[1]

# 폴더 안에서 rbcL_ 로 시작하고 .gb 로 끝나는 파일만 고른다
names = []
for name in sorted(os.listdir(folder)):
    if name.startswith("rbcL_") and name.endswith(".gb"):
        names.append(name)

print("file\tversion\torganism\tcds_location\tcodon_start\tsame")

for name in names:
    path = os.path.join(folder, name)
    rec = SeqIO.read(path, "genbank")

    version = rec.id
    organism = rec.annotations["organism"]

    for feature in rec.features:
        if feature.type != "CDS":
            continue

        # CDS 위치에 해당하는 염기서열을 잘라 낸다
        cds_seq = feature.extract(rec.seq)

        # codon_start 가 2나 3이면 그만큼 앞을 건너뛰고 번역을 시작한다
        codon_start = 1
        if "codon_start" in feature.qualifiers:
            codon_start = int(feature.qualifiers["codon_start"][0])
        cds_seq = cds_seq[codon_start - 1:]

        # 3의 배수 길이로 맞춘다 (부분 CDS는 끝이 잘려 있을 수 있다)
        length = len(cds_seq) - len(cds_seq) % 3
        cds_seq = cds_seq[:length]

        # table=11 (세균, 엽록체 코돈표)로 번역하고 끝의 종결 코돈 * 를 뺀다
        protein = str(cds_seq.translate(table=11))
        if protein.endswith("*"):
            protein = protein[:-1]

        translation = feature.qualifiers["translation"][0]
        same = protein == translation

        print(name + "\t" + version + "\t" + organism + "\t" +
              str(feature.location) + "\t" + str(codon_start) + "\t" + str(same))
