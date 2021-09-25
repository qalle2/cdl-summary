# Warning: this script overwrites files.

rm -f test-out/*.csv
rm -f test-out/*.txt

python3 cdl_summary.py -r16 -b16        cdl/gamegenie.cdl > test-out/gamegenie-prg-default.csv
python3 cdl_summary.py -r16 -b16 -ft    cdl/gamegenie.cdl > test-out/gamegenie-prg-default.txt
python3 cdl_summary.py -r16 -b16 -m -fc cdl/gamegenie.cdl > test-out/gamegenie-prg-nomethod.csv
python3 cdl_summary.py -r16 -b16 -m -ft cdl/gamegenie.cdl > test-out/gamegenie-prg-nomethod.txt

python3 cdl_summary.py --prg-size 32     -b32    -ft cdl/smb.cdl > test-out/smb-prg-default.txt
python3 cdl_summary.py --prg-size 32     -b32 -m -ft cdl/smb.cdl > test-out/smb-prg-nomethod.txt
python3 cdl_summary.py --prg-size 32 -pc -b8     -ft cdl/smb.cdl > test-out/smb-chr.txt

python3 cdl_summary.py --prg-size 128 -pp -b16     -ft cdl/blaster.cdl > test-out/blaster-prg.txt
python3 cdl_summary.py --prg-size 128 -pc -b4  -o4 -ft cdl/blaster.cdl > test-out/blaster-chr.txt

echo "test-out/:"
ls -1 test-out/
