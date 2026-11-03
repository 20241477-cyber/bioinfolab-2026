#!/bin/bash
# 식물 8종의 rbcL 서열을 NCBI E-utilities로 받아 FASTA(.fa)와 GenBank(.gb)로 저장한다.
# 사용법: bash src/get_rbcL.sh      (lab10 폴더에서 실행)

base="https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# 한 줄에 "학명(공백은 +로)  파일이름"
while read name file
do
    echo "== $name -> $file"

    # 1) esearch: 첫 번째 결과의 ID만 받는다
    wget -q -O data/${file}_search.xml \
      "$base/esearch.fcgi?db=nucleotide&retmax=1&term=${name}[ORGN]+AND+rbcL[GENE]+AND+1300:1500[SLEN]"
    sleep 1

    id=$(grep -o '<Id>[0-9]*</Id>' data/${file}_search.xml | head -n 1 | sed 's/<[^>]*>//g')

    # ID가 없으면 이 종은 건너뛴다
    if [ -z "$id" ]
    then
        echo "   오류: $name 의 검색 결과에 ID가 없어 건너뜁니다." >&2
        continue
    fi
    echo "   ID: $id"

    # 2) efetch: FASTA와 GenBank를 각각 받는다
    wget -q -O data/${file}.fa "$base/efetch.fcgi?db=nucleotide&id=$id&rettype=fasta&retmode=text"
    sleep 1
    wget -q -O data/${file}.gb "$base/efetch.fcgi?db=nucleotide&id=$id&rettype=gb&retmode=text"
    sleep 1
done << END
Arabidopsis+thaliana        rbcL_arabidopsis
Panax+ginseng               rbcL_ginseng
Oryza+sativa                rbcL_rice
Zea+mays                    rbcL_maize
Ginkgo+biloba               rbcL_ginkgo
Pinus+thunbergii            rbcL_pine
Adiantum+capillus-veneris   rbcL_fern
Marchantia+polymorpha       rbcL_liverwort
END
