# cdl-summary
```
usage: cdl_summary.py [-h] [-p {p,c}] [-o {0,1,2,3,4,5,6,7,32,40,48,56}] [-b {1,2,4,8,16,32}] input_file prg_size

Print an FCEUX Code/Data Logger file (.cdl) in human-readable format.

positional arguments:
  input_file            The .cdl file to read. Size: 16-6136 KiB and a multiple of 8 KiB.
  prg_size              The PRG ROM size of the input file, in KiB (16-4096 and a multiple of 16, usually a power of
                        two).

optional arguments:
  -h, --help            show this help message and exit
  -p {p,c}, --part {p,c}
                        Which part to read from the input file. p=PRG ROM (default), c=CHR ROM.
  -o {0,1,2,3,4,5,6,7,32,40,48,56}, --origin {0,1,2,3,4,5,6,7,32,40,48,56}
                        The CPU/PPU address each ROM bank starts from, in KiB. 32/40/48/56 for PRG ROM (default=32),
                        0-7 for CHR ROM (default=0).
  -b {1,2,4,8,16,32}, --bank-size {1,2,4,8,16,32}
                        Size of PRG/CHR ROM banks in KiB. 8/16/32 for PRG ROM (default=16), 1/2/4/8 for CHR ROM
                        (default=8). -o plus -b must be 64 or less for PRG ROM and 8 or less for CHR ROM.
```

## Examples
```
C:\>python cdl_summary.py --part p --origin 32 --bank-size 32 smb.cdl 32
"PRG address","CPU bank","offset in bank","CPU address","block length","CDL byte","description"
0,0,0,32768,90,1,"code"
90,0,90,32858,7,2,"data"
97,0,97,32865,1,0,"unaccessed"
98,0,98,32866,18,2,"data"
116,0,116,32884,1,0,"unaccessed"
(snip)
```

```
C:\>python cdl_summary.py --part c --origin 0 --bank-size 8 cdl\smb.cdl 32
"CHR address","PPU bank","offset in bank","PPU address","block length","CDL byte","description"
0,0,0,0,4336,1,"rendered"
4336,0,4336,4336,16,0,"unaccessed"
4352,0,4352,4352,48,1,"rendered"
4400,0,4400,4400,16,0,"unaccessed"
(snip)
```
