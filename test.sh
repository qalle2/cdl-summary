clear

#echo "=== Excitebike, PRG ROM ==="
#python3 cdl_summary.py --prg-size 16 --part p --origin 48 --bank-size 16 cdl/excite.cdl
#echo

#echo "=== Excitebike, CHR ROM ==="
#python3 cdl_summary.py --prg-size 16 --part c --origin 0 --bank-size 8 cdl/excite.cdl
#echo

echo "=== SMB, PRG ROM ==="
python3 cdl_summary.py --prg-size 32 --part p --origin 32 --bank-size 32 cdl/smb.cdl
echo

echo "=== SMB, CHR ROM ==="
python3 cdl_summary.py --prg-size 32 --part c --origin 0 --bank-size 8 cdl/smb.cdl
echo

#echo "=== Blaster Master, PRG ROM ==="
#python3 cdl_summary.py --prg-size 128 --part p --origin 32 --bank-size 16 cdl/blaster.cdl
#echo

#echo "=== Blaster Master, CHR ROM ==="
#python3 cdl_summary.py --prg-size 128 --part c --origin 0 --bank-size 4 cdl/blaster.cdl
#echo
