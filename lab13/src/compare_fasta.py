# 목적: 직접 추출한 유전자 FASTA 파일과 Prokka의 FFN 파일에서
#       같은 유전자의 염기서열을 꺼내 서로 같은지 비교한다.
#       FASTA 헤더와 줄바꿈은 비교하지 않고 실제 DNA 염기서열만 비교한다.
# 사용법: python3 src/compare_fasta.py <추출한 FASTA 파일> <Prokka FFN 파일> <유전자 ID>
# 예시:   python3 src/compare_fasta.py phnD2.fasta doc/prokka_out/sample.ffn EIHNLLIJ_00001

import sys
import os

# lab07/src/fasta.py의 read_fasta() 함수를 가져온다
# 이 파일 위치(lab13/src)에서 두 단계 위로 올라가 lab07/src 폴더를 찾는다
this_folder = os.path.dirname(os.path.abspath(__file__))
lab07_src = os.path.join(this_folder, "..", "..", "lab07", "src")
sys.path.append(lab07_src)
from fasta import read_fasta

# 1. 명령행 인자 확인
if len(sys.argv) < 4:
    print("사용법: python3 compare_fasta.py <추출한 FASTA 파일> <Prokka FFN 파일> <유전자 ID>")
    sys.exit(1)

fasta_file = sys.argv[1]
ffn_file = sys.argv[2]
gene_id = sys.argv[3]

# 2. 두 파일을 읽는다
#    read_fasta()는 헤더의 첫 단어(ID)를 이름으로, 줄바꿈 없이 이어 붙인 서열을 값으로 돌려준다
#    그래서 헤더의 설명 부분과 줄바꿈은 자동으로 비교에서 빠진다
fasta_seqs = read_fasta(fasta_file)
ffn_seqs = read_fasta(ffn_file)

# 유전자 ID가 각 파일에 있는지 확인한다
if gene_id not in fasta_seqs:
    print("오류: " + fasta_file + " 에서 " + gene_id + " 를 찾을 수 없습니다.")
    sys.exit(1)
if gene_id not in ffn_seqs:
    print("오류: " + ffn_file + " 에서 " + gene_id + " 를 찾을 수 없습니다.")
    sys.exit(1)

# 3. 실제 염기서열만 꺼낸다 (대소문자 차이는 무시하기 위해 모두 대문자로 바꾼다)
seq1 = fasta_seqs[gene_id].upper()
seq2 = ffn_seqs[gene_id].upper()

# 4. 두 서열의 길이를 출력한다
print("유전자 ID: " + gene_id)
print(fasta_file + " 길이: " + str(len(seq1)) + " bp")
print(ffn_file + " 길이: " + str(len(seq2)) + " bp")

# 5. 일치 여부를 출력하고, 다르면 처음 다른 위치를 찾는다
if seq1 == seq2:
    print("결과: 두 서열이 완전히 일치합니다.")
else:
    print("결과: 두 서열이 일치하지 않습니다.")

    # 짧은 서열의 길이만큼 한 글자씩 비교한다
    shorter = min(len(seq1), len(seq2))
    first_diff = -1
    for i in range(shorter):
        if seq1[i] != seq2[i]:
            first_diff = i
            break

    if first_diff != -1:
        # 위치는 사람이 읽기 쉽게 1부터 센다
        print("처음 다른 위치: " + str(first_diff + 1) + "번째 염기 ("
              + fasta_file + ": " + seq1[first_diff] + ", "
              + ffn_file + ": " + seq2[first_diff] + ")")
    else:
        # 겹치는 부분은 모두 같고 길이만 다른 경우
        print("처음 다른 위치: " + str(shorter + 1) + "번째 염기 (한쪽 서열이 여기서 끝남)")
