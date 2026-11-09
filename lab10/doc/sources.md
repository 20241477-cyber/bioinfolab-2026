# rbcL 서열 데이터 출처

| 파일 | VERSION | ORGANISM | 길이(bp) | CDS 위치 | codon_start | 번역 검증 | 확인 방법 | 문제 |
|---|---|---|---|---|---|---|---|---|
| rbcL_arabidopsis | KU739560.1 | Arabidopsis thaliana | 1408 | [<0:>1408](+) | 2 | True | fasta.py, grep, check_cds.py | 없음 |
| rbcL_rice | L24073.1 | Oryza sativa | 1355 | [34:1240](+) | 1 | True | fasta.py, grep, check_cds.py | 없음 |
| rbcL_maize | Z11973.1 | Zea mays | 1431 | [0:1431](+) | 1 | True | fasta.py, grep, check_cds.py | 없음 |
| rbcL_ginkgo | KF221173.1 | Ginkgo biloba | 1317 | [<0:>1317](+) | 1 | True | fasta.py, grep, check_cds.py | 없음 |
| rbcL_pine | JQ512595.1 | Pinus thunbergii | 1428 | [0:1428](+) | 1 | True | fasta.py, grep, check_cds.py | 없음 |
| rbcL_fern | MW620303.1 | Adiantum capillus-veneris | 1308 | [<0:>1308](+) | 1 | True | fasta.py, grep, check_cds.py | 없음 |
| rbcL_liverwort | LC536762.1 | Marchantia polymorpha subsp. ruderalis | 1399 | [<0:1399](+) | 2 | True | fasta.py, grep, check_cds.py | 요청한 Marchantia polymorpha와 달리 ORGANISM에 아종명(subsp. ruderalis)이 추가되어 있음 |

## 확인 방법

- **fasta.py**: 서열 길이 및 GC 비율 확인
- **grep**: FASTA 서열 개수, GenBank의 VERSION 및 ORGANISM 확인
- **check_cds.py**: CDS 위치, codon_start 및 번역 결과 검증
