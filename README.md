# cdl-summary
```
usage: cdl_summary.py [-h] -r PRG_SIZE [-p {p,c}] -b {1,2,4,8,16,32}
                      [-o {0,1,2,3,4,5,6,7,32,40,48,56}] [-m] [-f {t,c}]
                      input_file

Print an FCEUX Code/Data Logger file (.cdl) in human-readable format.

positional arguments:
  input_file            The .cdl file to read. Size: 16-6136 KiB and a multiple of 8 KiB.

optional arguments:
  -h, --help            show this help message and exit
  -r PRG_SIZE, --prg-size PRG_SIZE
                        PRG ROM size of input file, in KiB (16-4096 and a multiple of 16, usually
                        a power of two). Required.
  -p {p,c}, --part {p,c}
                        Which part to read from input file. 'p'=PRG ROM, 'c'=CHR ROM. Default='p'.
  -b {1,2,4,8,16,32}, --bank-size {1,2,4,8,16,32}
                        Size of ROM banks in KiB. 8/16/32 for PRG ROM, 1/2/4/8 for CHR ROM.
                        Required.
  -o {0,1,2,3,4,5,6,7,32,40,48,56}, --origin {0,1,2,3,4,5,6,7,32,40,48,56}
                        The CPU/PPU address each ROM bank starts from, in KiB. For PRG ROM:
                        32/40/48/56 but not greater than 64 minus --bank-size; default=maximum.
                        For CHR ROM: 0-7 but not greater than 8 minus --bank-size; default=0.
  -m, --ignore-access-method
                        Ignore how PRG ROM bytes were accessed (directly/indirectly/as PCM audio).
  -f {t,c}, --output-format {t,c}
                        Output format. 'c' = CSV (fields separated by commas, numbers in decimal,
                        strings quoted); 't'=tabular (constant-width fields, numbers in
                        hexadecimal). Default='c'.
```

## Sample CDL files

There are some CDL files under `cdl/`.

Percentage of unlogged bytes (lower is better):
* blastermaster-u.cdl: 19%
* daysofthunder-u.cdl: 9%
* drmario-ju-prg0.cdl: 14%
* drmario-ju-prg1.cdl: 18%
* excitebike-ju.cdl: 6%
* gamegenie.cdl: 82%
* golf-u.cdl: 3%
* lunarpool-u.cdl: 14%
* smb1-w.cdl: 1%

## Examples

PRG ROM &ndash; CSV output:
```
$ python3 cdl_summary.py --prg-size 16 --bank-size 16 cdl/gamegenie.cdl
"ROM address","bank","offset in bank","NES address","CDL byte repeat count","CDL byte","CDL byte description"
0,0,0,49152,13,2,"data"
13,0,13,49165,12275,0,"unaccessed"
12288,0,12288,61440,41,9,"code"
12329,0,12329,61481,1,11,"code, data"
12330,0,12330,61482,228,9,"code"
12558,0,12558,61710,1,11,"code, data"
12559,0,12559,61711,107,9,"code"
12666,0,12666,61818,1,11,"code, data"
12667,0,12667,61819,62,9,"code"
12729,0,12729,61881,1,11,"code, data"
12730,0,12730,61882,140,9,"code"
12870,0,12870,62022,2,0,"unaccessed"
12872,0,12872,62024,19,9,"code"
12891,0,12891,62043,1,11,"code, data"
(snip)
```

PRG ROM &ndash; tabular output:
```
$ python3 cdl_summary.py --prg-size 16 --bank-size 16 --output-format t cdl/gamegenie.cdl
ROM address, bank, offset in bank, NES address, CDL byte repeat count, CDL byte, CDL byte description (all numbers in hexadecimal):
000000 00 0000 c000 000d 02 data
00000d 00 000d c00d 2ff3 00 unaccessed
003000 00 3000 f000 0029 09 code
003029 00 3029 f029 0001 0b code, data
00302a 00 302a f02a 00e4 09 code
00310e 00 310e f10e 0001 0b code, data
00310f 00 310f f10f 006b 09 code
00317a 00 317a f17a 0001 0b code, data
00317b 00 317b f17b 003e 09 code
0031b9 00 31b9 f1b9 0001 0b code, data
0031ba 00 31ba f1ba 008c 09 code
003246 00 3246 f246 0002 00 unaccessed
003248 00 3248 f248 0013 09 code
00325b 00 325b f25b 0001 0b code, data
(snip)
```
