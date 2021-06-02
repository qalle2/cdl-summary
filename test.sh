clear

echo "=== Excitebike, PRG ROM ==="
python3 cdl_summary.py --prg-size 16 --bank-size 16 cdl/excite.cdl
echo

echo "=== Excitebike, CHR ROM ==="
python3 cdl_summary.py --prg-size 16 --part c --bank-size 8 cdl/excite.cdl
echo

echo "=== SMB, PRG ROM, verbose ==="
python3 cdl_summary.py --prg-size 32 --bank-size 32 --verbose cdl/smb.cdl
echo

echo "=== SMB, PRG ROM, ignore access method, verbose ==="
python3 cdl_summary.py --prg-size 32 --bank-size 32 --ignore-access-method --verbose cdl/smb.cdl
echo

echo "=== SMB, CHR ROM, verbose ==="
python3 cdl_summary.py --prg-size 32 --part c --bank-size 8 --verbose cdl/smb.cdl
echo

echo "=== Blaster Master, PRG ROM ==="
python3 cdl_summary.py --prg-size 128 --part p --bank-size 16 --origin 32 cdl/blaster.cdl
echo

echo "=== Blaster Master, CHR ROM ==="
python3 cdl_summary.py --prg-size 128 --part c --bank-size 4 --origin 0 cdl/blaster.cdl
echo
