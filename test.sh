clear

echo "=== Game Genie, PRG ROM, ignore access method, verbose ==="
python3 cdl_summary.py --prg-size 16 --bank-size 16 --ignore-access-method --verbose cdl/gamegenie.cdl
echo

echo "=== SMB, PRG ROM ==="
python3 cdl_summary.py --prg-size 32 --bank-size 32 cdl/smb.cdl
echo

echo "=== SMB, CHR ROM ==="
python3 cdl_summary.py --prg-size 32 --part c --bank-size 8 cdl/smb.cdl
echo

echo "=== Blaster Master, PRG ROM (2nd bank only) ==="
python3 cdl_summary.py --prg-size 128 --part p --bank-size 16 --origin 32 cdl/blaster.cdl | grep "^[0-9]\+,1,"
echo

echo "=== Blaster Master, CHR ROM (2nd bank only) ==="
python3 cdl_summary.py --prg-size 128 --part c --bank-size 4 --origin 0 cdl/blaster.cdl | grep "^[0-9]\+,1,"
echo
