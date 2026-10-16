"""FASTA 파일을 다루는 함수 모음"""

 
def read_fasta(filename):
    """FASTA 파일을 읽어 {이름: 서열} 딕셔너리로 돌려준다."""
    seqs = {}
    name = None
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith(">"):
                name = line[1:].split()[0]
                seqs[name] = ""
            else:
                seqs[name] = seqs[name] + line
    return seqs
 
 
def gc_content(seq):
    """서열의 GC 비율을 0과 1 사이의 수로 돌려준다."""
    if len(seq) == 0:
        return 0.0
    gc = seq.count("G") + seq.count("C")
    return gc / len(seq)
 
def write_fasta(seqs, filename):
    """{이름: 서열} 딕셔너리를 FASTA 파일로 저장한다."""
    with open(filename, "w") as out:
        for name in seqs:
            out.write(">" + name + "\n")
            out.write(seqs[name] + "\n")

def reverse_complement(seq):
    """서열의 역상보 서열을 돌려준다."""
    seq = seq.upper()

    complement = {
        "A": "T",
        "T": "A",
        "G": "C",
        "C": "G" }

    reverse_seq = ""

    for base in seq:
        reverse_seq = reverse_seq + complement[base]

    reverse_seq = reverse_seq[::-1]

    return reverse_seq


def length_stats(seqs):
    """서열의 길이 통계를 딕셔너리로 반환한다."""

    lengths = [] # 서열 별 길이를 담은 리스트

    for name in seqs:
        lengths.append(len(seqs[name]))

    stats = {
        "count": len(seqs),
        "total": sum(lengths),
        "average": sum(lengths) / len(lengths),
        "min": min(lengths),
        "max": max(lengths) }

    return stats

if __name__ == "__main__":
    import sys

    # 기존 GC 비율 확인 코드
    seqs = read_fasta(sys.argv[1])

    for name in seqs:
        print(name, len(seqs[name]), round(gc_content(seqs[name]), 3))
    
    # 역상보 서열을 두 번 구하면 원래 서열로 돌아오는지 확인
    for name in seqs:
        seq = seqs[name]
        print(name, reverse_complement(reverse_complement(seq)) == seq)
