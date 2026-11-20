import sys
 
def read_fasta(filename):
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
 
def n50(lengths):
    lengths = sorted(lengths, reverse=True)
    total = sum(lengths)
    half = total / 2
 
    running = 0
    for length in lengths:
        running = running + length
        if running >= half:
            return length
 
seqs = read_fasta(sys.argv[1])
lengths = []
for name in seqs:
    lengths.append(len(seqs[name]))
 
print("contig 개수:", len(lengths))
print("전체 길이:", sum(lengths))
print("가장 긴 contig:", max(lengths))
print("N50:", n50(lengths))

# 모든 contig 길이를 내림차순으로 정렬하여 한 줄에 하나씩 저장한다
sorted_lengths = sorted(lengths, reverse=True)
out = open("doc/contig_lengths.txt", "w")
for length in sorted_lengths:
    out.write(str(length) + "\n")
out.close()
print("contig 길이 저장: doc/contig_lengths.txt")
