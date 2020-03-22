@echo off
cls

echo === test.bat: Excitebike, PRG ROM ===
python cdl_summary.py --prg-size 16 --part p --origin 48 --bank-size 16 cdl\excite.cdl
if errorlevel 1 goto error
echo.

echo === test.bat: Excitebike, CHR ROM ===
python cdl_summary.py --prg-size 16 --part c --origin 0 --bank-size 8 cdl\excite.cdl
if errorlevel 1 goto error
echo.

echo === test.bat: SMB, PRG ROM ===
python cdl_summary.py --prg-size 32 --part p --origin 32 --bank-size 32 cdl\smb.cdl
if errorlevel 1 goto error
echo.

echo === test.bat: SMB, CHR ROM ===
python cdl_summary.py --prg-size 32 --part c --origin 0 --bank-size 8 cdl\smb.cdl
if errorlevel 1 goto error
echo.

echo === test.bat: Blaster Master, PRG ROM ===
python cdl_summary.py --prg-size 128 --part p --origin 32 --bank-size 16 cdl\blaster.cdl
if errorlevel 1 goto error
echo.

echo === test.bat: Blaster Master, CHR ROM ===
python cdl_summary.py --prg-size 128 --part c --origin 0 --bank-size 4 cdl\blaster.cdl
if errorlevel 1 goto error
goto end

:error
echo === test.bat: error ===
goto end

:end
