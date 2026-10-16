import sys
from fasta import read_fasta, length_stats

infile = sys.argv[1]

seqs = read_fasta(infile)
stats = length_stats(seqs)

print("Sequence count:", stats["count"])
print("Total length:", stats["total"])
print("Average length:", round(stats["average"], 2))
print("Minimum length:", stats["min"])
print("Maximum length:", stats["max"])

