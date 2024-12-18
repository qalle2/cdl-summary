# Warning: this script overwrites files.

clear
rm -f test-out/*.csv
rm -f test-out/*.txt
rm -f test-out/*.png

echo "=== Testing cdl_summary.py ==="

python3 cdl_summary.py \
    --prg-size 16 \
    cdl/gamegenie.cdl > test-out/gamegenie-prg-default.csv
python3 cdl_summary.py \
    --prg-size 16 --output-format t \
    cdl/gamegenie.cdl > test-out/gamegenie-prg-default.txt
python3 cdl_summary.py \
    --prg-size 16 --ignore-access-method --output-format c \
    cdl/gamegenie.cdl > test-out/gamegenie-prg-nomethod.csv
python3 cdl_summary.py \
    --prg-size 16 --ignore-access-method --output-format t \
    cdl/gamegenie.cdl > test-out/gamegenie-prg-nomethod.txt

python3 cdl_summary.py \
    --prg-size 32 --output-format t \
    cdl/smb1-w.cdl > test-out/smb-prg-default.txt
python3 cdl_summary.py \
    --prg-size 32 --ignore-access-method --output-format t \
    cdl/smb1-w.cdl > test-out/smb-prg-nomethod.txt
python3 cdl_summary.py \
    --prg-size 32 --part c --output-format t \
    cdl/smb1-w.cdl > test-out/smb-chr.txt

python3 cdl_summary.py \
    --prg-size 128 --part p --bank-size 16 --output-format t \
    cdl/blastermaster-u.cdl > test-out/blaster-prg.txt
python3 cdl_summary.py \
    --prg-size 128 --part c --bank-size 4 --output-format t \
    cdl/blastermaster-u.cdl > test-out/blaster-chr.txt

echo

echo "=== Testing cdl2png.py ==="
python3 cdl2png.py cdl/gamegenie.cdl       test-out/gamegenie.png
python3 cdl2png.py cdl/smb1-w.cdl          test-out/smb1-w.png
python3 cdl2png.py cdl/blastermaster-u.cdl test-out/blastermaster-u.png
echo

echo "=== test-out/ (verify manually) ==="
ls -1 test-out/
echo
