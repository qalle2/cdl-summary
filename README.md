# cdl-summary
Note: not tested since last update; get the previous version if this one doesn't work.
```
usage: cdl_summary.py [-h] [-g PRG_ROM_SIZE] [-p {p,c}] [-o {0,1,2,3,4,5,6,7,32,40,48,56}] [-r {0,1,2,4,8,16,32}] [-m]
                      [-d] [-a] [-b]
                      input_file

Print an FCEUX Code/Data Logger file (.cdl) in human-readable format.

positional arguments:
  input_file            The .cdl file to read. Size: 16-6136 KiB and a multiple of 8 KiB.

optional arguments:
  -h, --help            show this help message and exit
  -g PRG_ROM_SIZE, --prg_rom_size PRG_ROM_SIZE
                        The PRG ROM size of the input file, in KiB (16-4096 and a multiple of 16, usually a power of
                        two). Omit to guess.
  -p {p,c}, --part {p,c}
                        Which part to read from the input file. p=PRG ROM (default), c=CHR ROM. -d/-a/-b can't be used
                        with CHR ROM.
  -o {0,1,2,3,4,5,6,7,32,40,48,56}, --origin {0,1,2,3,4,5,6,7,32,40,48,56}
                        The CPU/PPU address each ROM bank starts from, in KiB. 32/40/48/56 for PRG ROM (default=32),
                        0-7 for CHR ROM (default=0).
  -r {0,1,2,4,8,16,32}, --bank-size {0,1,2,4,8,16,32}
                        Size of PRG/CHR ROM banks in KiB. 8/16/32 for PRG ROM (default=32), 1/2/4/8 for CHR ROM
                        (default=8). -o plus -r must be 64 or less for PRG ROM and 8 or less for CHR ROM.
  -m, --ignore-method   Ignore how bytes were accessed. Overrides -d/-a/-b.
  -d, --ignore-directness
                        Ignore whether PRG ROM bytes were accessed directly or indirectly.
  -a, --ignore-pcm      Ignore whether PRG ROM bytes were accessed as PCM audio data.
  -b, --ignore-bank     Ignore which CPU bank PRG ROM bytes were mapped to when last accessed.
```

## Example
```
python cdl_summary.py excitebike.cdl
Warning: guessing PRG bank size: 16384 bytes
0,0,0,49152,8,10,"data, last mapped to CPU bank 0xc000-0xffff"
8,0,8,49160,8,0,"unaccessed"
16,0,16,49168,16,10,"data, last mapped to CPU bank 0xc000-0xffff"
32,0,32,49184,4,0,"unaccessed"
36,0,36,49188,10,10,"data, last mapped to CPU bank 0xc000-0xffff"
46,0,46,49198,1,0,"unaccessed"
47,0,47,49199,8,10,"data, last mapped to CPU bank 0xc000-0xffff"
55,0,55,49207,1,0,"unaccessed"
```
