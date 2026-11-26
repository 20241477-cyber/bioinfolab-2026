# 목적: DNA 서열의 6개 해독틀(정방향 3개 + 역상보 3개)에서 ORF(ATG ~ 종결 코돈)를 찾는다.
# 사용법: python3 src/find_orf.py <DNA서열>
# 좌표는 파이썬 슬라이스 방식(0부터 시작, 끝 좌표는 포함하지 않음)이다.
import sys
 
STOPS = ["TAA", "TAG", "TGA"]
 
def find_orfs(seq, frame):
    orfs = []
    start = None
 
    for i in range(frame, len(seq) - 2, 3):
        codon = seq[i:i + 3]
 
        if codon == "ATG" and start is None:
            start = i
        elif codon in STOPS and start is not None:
            orfs.append((start, i + 3))
            start = None
 
    return orfs

# 역상보 서열을 만든다: 서열을 뒤에서부터 읽으면서 각 염기를 상보 염기로 바꾼다.
def reverse_complement(seq):
    rc = ""
    for i in range(len(seq) - 1, -1, -1):
        base = seq[i]
        if base == "A":
            rc = rc + "T"
        elif base == "T":
            rc = rc + "A"
        elif base == "G":
            rc = rc + "C"
        elif base == "C":
            rc = rc + "G"
        else:
            rc = rc + "N"
    return rc
 
seq = sys.argv[1].upper()
rc_seq = reverse_complement(seq)
n = len(seq)

print("=== 정방향 (+) ===")
for frame in [0, 1, 2]:
    orfs = find_orfs(seq, frame)
    print("틀 +" + str(frame + 1), ":", orfs)
    for s, e in orfs:
        print("   ", seq[s:e], "시작", s, "끝", e, "길이", e - s)

print("=== 역방향 (-, 역상보 서열) ===")
for frame in [0, 1, 2]:
    orfs = find_orfs(rc_seq, frame)
    print("틀 -" + str(frame + 1), ":", orfs)
    for s, e in orfs:
        # 역상보 서열의 좌표 (s, e)를 원래 서열의 좌표로 바꾼다.
        orig_s = n - e
        orig_e = n - s
        print("   ", rc_seq[s:e], "시작", s, "끝", e, "길이", e - s,
              "(원래 서열 기준:", orig_s, "~", orig_e, ")")
