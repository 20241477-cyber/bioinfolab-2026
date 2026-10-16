import sys
import glob
from fasta import read_fasta, gc_content, length_stats

folder = sys.argv[1]
outfile = sys.argv[2]

with open(outfile, "w") as out:
    out.write("file\tcount\ttotal\tavg_gc\n")

    for path in sorted(glob.glob(folder + "/*.fasta")):
        seqs = read_fasta(path)

        stats = length_stats(seqs)
        count = stats["count"]
        total = stats["total"]

        gc_total = 0
        for name in seqs:
            gc_total = gc_total + gc_content(seqs[name])

        avg_gc = gc_total / count

        out.write(path + "\t" + str(count) + "\t"
                  + str(total) + "\t" + str(round(avg_gc, 4)) + "\n")
