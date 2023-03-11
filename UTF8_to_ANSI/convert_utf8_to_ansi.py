import glob
import os

for d in ('in', 'out', 'done', 'error'):
    os.makedirs(d, exist_ok=True)  # = mkdir -p

for f in glob.glob("in/*.*"):
    (filepath, fileName) = os.path.split(f)
    print(fileName)

    try:
        with open(f, mode='r', encoding='utf-8') as fh:
            cont = fh.read()

        with open(f"out/{fileName}", mode='w', encoding='ansi', newline='\r\n') as fh:
            fh.write(cont)
        os.rename(f, f"done/{fileName}")
    except UnicodeEncodeError:
        os.rename(f, f"error/{fileName}")
        print(f"ERROR converting '{fileName}' from UTF-8 to ANSI")
