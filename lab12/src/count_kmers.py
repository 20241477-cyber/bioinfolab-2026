#!/usr/bin/env python3
# count_kmers.py — 길이가 L인 서열에서 k-mer의 개수를 계산한다
# 사용법: python3 src/count_kmers.py
#
# 길이 L인 서열에서 k-mer는 위치 0, 1, ..., L-k 에서 시작할 수 있으므로
# k-mer의 개수는 L - k + 1 개이다.


def count_kmers(L, k):
    # k가 L보다 크면 길이 k인 조각을 만들 수 없으므로 0을 반환한다
    if k > L:
        return 0
    return L - k + 1

# (L, k, 직접 계산한 값)
# (10, 5): 10 - 5 + 1 = 6
# (8, 3) :  8 - 3 + 1 = 6
# (5, 5) :  5 - 5 + 1 = 1
# (5, 7) : 길이 7인 조각을 길이 5인 서열에서 꺼낼 수 없으므로 실제 개수는 0
tests = [(10, 5, 6), (8, 3, 6), (5, 5, 1), (5, 7, 0)]

print("L\tk\t직접계산\t함수결과\t일치")
for t in tests:
    L = t[0]
    k = t[1]
    expected = t[2]
    result = count_kmers(L, k)
    if result == expected:
        same = "O"
    else:
        same = "X"
    print(str(L) + "\t" + str(k) + "\t" + str(expected) + "\t" + str(result) + "\t" + same)
