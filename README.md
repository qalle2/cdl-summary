# cdl-summary
```
usage: cdl_summary.py [-h] -r PRG_SIZE -p {p,c} -o {0,1,2,3,4,5,6,7,32,40,48,56} -b
                      {1,2,4,8,16,32}
                      input_file

Print an FCEUX Code/Data Logger file (.cdl) in human-readable format. All options are required.

positional arguments:
  input_file            The .cdl file to read. Size: 16-6136 KiB and a multiple of 8 KiB.

optional arguments:
  -h, --help            show this help message and exit
  -r PRG_SIZE, --prg-size PRG_SIZE
                        PRG ROM size of input file, in KiB (16-4096 and a multiple of 16, usually
                        a power of two).
  -p {p,c}, --part {p,c}
                        Which part to read from input file. p=PRG ROM, c=CHR ROM.
  -o {0,1,2,3,4,5,6,7,32,40,48,56}, --origin {0,1,2,3,4,5,6,7,32,40,48,56}
                        The CPU/PPU address each ROM bank starts from, in KiB. 32/40/48/56 for PRG
                        ROM, 0-7 for CHR ROM.
  -b {1,2,4,8,16,32}, --bank-size {1,2,4,8,16,32}
                        Size of PRG/CHR ROM banks in KiB. 8/16/32 for PRG ROM, 1/2/4/8 for CHR
                        ROM. -o plus -b must be 64 or less for PRG ROM and 8 or less for CHR ROM.
```

## Examples
```
python3 cdl_summary.py --prg-size 32 --part p --origin 32 --bank-size 32 smb.cdl
"PRG address","CPU bank","offset in bank","CPU address","block length","CDL byte","description"
0,0,0,32768,90,1,"code"
90,0,90,32858,7,2,"data"
97,0,97,32865,1,0,"unaccessed"
98,0,98,32866,18,2,"data"
116,0,116,32884,1,0,"unaccessed"
117,0,117,32885,13,2,"data"
130,0,130,32898,406,1,"code"
536,0,536,33304,8,34,"data (indirectly accessed)"
544,0,544,33312,17,1,"code"
561,0,561,33329,3,17,"code (indirectly accessed)"
(snip)
```

```
python3 cdl_summary.py --prg-size 32 --part c --origin 0 --bank-size 8 smb.cdl
"CHR address","PPU bank","offset in bank","PPU address","block length","CDL byte","description"
0,0,0,0,4336,1,"rendered"
4336,0,4336,4336,16,0,"unaccessed"
4352,0,4352,4352,48,1,"rendered"
4400,0,4400,4400,16,0,"unaccessed"
4416,0,4416,4416,208,1,"rendered"
4624,0,4624,4624,16,0,"unaccessed"
4640,0,4640,4640,1920,1,"rendered"
6560,0,6560,6560,16,0,"unaccessed"
6576,0,6576,6576,1296,1,"rendered"
7872,0,7872,7872,314,2,"read programmatically"
8186,0,8186,8186,6,0,"unaccessed"
```
