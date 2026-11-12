# paired-end FASTQ 파일 두 개(_1, _2)가 서로 짝이 맞는지 확인한다.
# 1) 두 파일의 read 개수가 같은지 확인한다.
# 2) 같은 순서에 있는 read끼리 이름이 일치하는지 확인한다.
# read 이름 비교 방법:
#   - 헤더 줄(@로 시작)에서 첫 번째 공백 앞부분만 read ID로 사용한다.
#     예) "@SRR1553607.1 1 length=101" -> "SRR1553607.1"
#     예) "@M00123:45:000:1:1101:15589:1331 1:N:0:1" -> "M00123:45:000:1:1101:15589:1331"
#   - 예전 일루미나 형식처럼 ID 끝에 "/1", "/2"가 붙어 있으면 떼고 비교한다.
#     예) "@HWI-ST:8:1:1:1#0/1" -> "HWI-ST:8:1:1:1#0"
# 사용법: python3 src/check_paired.py <FASTQ_1> <FASTQ_2>
import sys

def read_names(filename):
    # FASTQ 파일에서 read마다 헤더 줄(4줄 중 첫 줄)만 모아 돌려준다
    names = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        header = lines[i].rstrip()
        if not header.startswith("@"):
            print("경고: " + filename + "의 " + str(i + 1) + "번째 줄이 @로 시작하지 않습니다: " + header)
        names.append(header[1:])    # 맨 앞의 @ 제거
    return names

def read_id(name):
    # 헤더에서 짝을 비교할 read ID만 뽑는다
    words = name.split()
    if len(words) == 0:
        return ""
    rid = words[0]                  # 첫 번째 공백 앞부분
    if rid.endswith("/1") or rid.endswith("/2"):
        rid = rid[:-2]              # 끝의 /1, /2 제거
    return rid

file1 = sys.argv[1]
file2 = sys.argv[2]

names1 = read_names(file1)
names2 = read_names(file2)

print("파일 1: " + file1)
print("파일 2: " + file2)
print()

# 1) read 개수 비교
count1 = len(names1)
count2 = len(names2)
print("[1] read 개수 확인")
print("  파일 1 read 개수: " + str(count1))
print("  파일 2 read 개수: " + str(count2))
if count1 == count2:
    count_ok = True
    print("  결과: 일치")
else:
    count_ok = False
    print("  결과: 불일치 (차이 " + str(abs(count1 - count2)) + "개)")
print()

# 2) 같은 순서의 read 이름 비교 (개수가 다르면 짧은 쪽 개수만큼 비교)
print("[2] 짝이 되는 read 이름 확인")
n = min(count1, count2)
mismatch = 0
for i in range(n):
    id1 = read_id(names1[i])
    id2 = read_id(names2[i])
    if id1 != id2:
        mismatch = mismatch + 1
        if mismatch <= 5:           # 처음 5개만 자세히 보여 준다
            print("  " + str(i + 1) + "번째 read 불일치: " + id1 + " / " + id2)

print("  비교한 read 쌍: " + str(n))
print("  이름이 일치한 쌍: " + str(n - mismatch))
print("  이름이 다른 쌍: " + str(mismatch))
if n > 0:
    print("  첫 번째 쌍 예시: " + names1[0] + "  |  " + names2[0])
    print("  비교에 쓴 ID: " + read_id(names1[0]) + "  |  " + read_id(names2[0]))
print()

# 최종 판정
print("[최종 결과]")
if count_ok and mismatch == 0:
    print("  두 파일은 짝이 맞는 paired-end FASTQ입니다.")
else:
    print("  두 파일의 짝이 맞지 않습니다.")
