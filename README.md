# cdl-summary
Prints a summary of a Code/Data Logger file (extension `.cdl`) created with the [NES](http://en.wikipedia.org/wiki/Nintendo_Entertainment_System) emulator [FCEUX](http://www.fceux.com).

## CDL files
A CDL file consists of two parts:
1. PRG-ROM log data (16 to 4080 KiB and a multiple of 16 KiB; often a power of two)
1. CHR-ROM log data (0 to 2040 KiB and a multiple of 8 KiB; often zero or a power of two)

See the FCEUX built-in help for more information on the file format.

## How to find out the PRG-ROM size of an iNES ROM file
The program needs to know how the PRG-ROM size of the CDL file (in 16-KiB banks).

1. Open the `.nes` file (*not* the `.cdl` file) in FCEUX.
2. Go to Help -> Message Log.
3. You should see something like: `PRG ROM: 2 x 16KiB`

# Examples

## PRG-ROM CDL data
```
C:\>python cdlsummary.py --prg-rom-banks=2 --part=p smb.cdl
Start address, end address, length, description:
(addresses in hexadecimal, lengths in decimal)
0000-0059 (   90): code, mapped to 0x8000-0x9fff
005a-0060 (    7): data, mapped to 0x8000-0x9fff
0061-0061 (    1): unaccessed
0062-0073 (   18): data, mapped to 0x8000-0x9fff
0074-0074 (    1): unaccessed
0075-0081 (   13): data, mapped to 0x8000-0x9fff
0082-0217 (  406): code, mapped to 0x8000-0x9fff
0218-021f (    8): data (indirectly accessed), mapped to 0x8000-0x9fff
0220-0230 (   17): code, mapped to 0x8000-0x9fff
0231-0233 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
(snip)
7f96-7ffd (  104): data, mapped to 0xe000-0xffff
7ffe-7fff (    2): unaccessed
```

## CHR-ROM CDL data
```
C:\>python cdlsummary.py --prg-rom-banks=2 --part=c smb.cdl
Start address, end address, length, description:
(addresses in hexadecimal, lengths in decimal)
0000-10ef (4336): rendered by PPU
10f0-10ff (  16): unaccessed
1100-112f (  48): rendered by PPU
1130-113f (  16): unaccessed
(snip)
1ec0-1ff9 ( 314): read programmatically
1ffa-1fff (   6): unaccessed
```
