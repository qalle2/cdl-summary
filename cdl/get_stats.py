import os

with os.scandir() as dirIter:
    files = [e.name for e in dirIter if e.is_file() and os.path.splitext(e.name)[1] == ".cdl"]

print("Percentage of unlogged bytes (lower is better):")
for filename in sorted(files):
    with open(filename, "rb") as handle:
        handle.seek(0)
        data = handle.read()
        ratio = sum(1 for b in data if b == 0) / len(data)
    print(f"* {filename}: {ratio*100:.0f}%")
