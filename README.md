# cdl-summary
Reads an [FCEUX](http://www.fceux.com) Code/Data Logger file (extension `.cdl`) and prints it with repeating bytes grouped together.

## Command line arguments

Syntax: *options* *input_file*

### *options*
* `-b` *size* or `--prg-rom-banks`=*size*
  * *size* is the PRG-ROM size of *input_file* in 16-KiB (16,384-byte) banks.
  * *size* must be 1 to 255.
  * This argument is required.
  * See below for how to find out the size.
* `-p` *part* or `--part`=*part*
  * Which part to read from *input_file* (case insensitive):
    * `P`: PRG-ROM (the default)
    * `C`: CHR-ROM
* `-o` *format* or `--output-format`=*format*
  * The output format (case insensitive):
    * `L`: long (human-readable, the default)
    * `S`: short (CSV, machine-readable)
* `--omit-unaccessed`
  * Exclude unaccessed bytes from the output.
* `--ignore-method`
  * Do not care whether bytes were accessed as PCM data, nor whether they were accessed indirectly or directly.
  * Only affects the PRG-ROM part.
* `--ignore-bank`
  * Do not care which bank PRG-ROM bytes were mapped to when last accessed.
  * Only affects the PRG-ROM part.

## How to find out the PRG-ROM size of a `.cdl` file

### Method 1: FCEUX
1. Find the iNES ROM file (extension `.nes`) that was used to create the `.cdl` file.
1. Open the `.nes` file in FCEUX.
1. Go to Help &rarr; Message Log.
1. You should see something like `PRG ROM: 2 x 16KiB` where `2` is the PRG-ROM size in 16-KiB banks.

### Method 2: hex editor
1. Find the iNES ROM file (extension `.nes`) that was used to create the `.cdl` file.
1. Open the `.nes` file in a hex editor.
1. The PRG-ROM size in 16-KiB banks is in offset 4 (the fifth byte, after the value `1A`).
1. Convert the value from hexadecimal to decimal with a calculator.

### Method 3: guessing
The PRG-ROM size is almost always a power of two, i.e., one of the following (in 16-KiB banks): 1, 2, 4, 8, 16, 32, 64, 128.

### *input_file*
  * The Code/Data Logger file to read.
  * The file size must be 16 KiB to 6,120 KiB and a multiple of 8 KiB.

## The structure of a `.cdl` file
A `.cdl` file consists of two parts:
1. PRG-ROM log data (16 KiB to 4,080 KiB and a multiple of 16 KiB)
1. CHR-ROM log data (0 bytes to 2,040 KiB and a multiple of 8 KiB)

See the FCEUX help (Help &rarr; Help&hellip; &rarr; Debug &rarR; Code/Data Logger) for more information on the file format.

## Examples

### PRG-ROM CDL data
```
python cdlsummary.py -b 2 -p p smb.cdl
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
0234-0236 (    3): code, mapped to 0x8000-0x9fff
0237-023e (    8): data (indirectly accessed), mapped to 0x8000-0x9fff
023f-0244 (    6): data, mapped to 0x8000-0x9fff
0245-0246 (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
0247-02df (  153): code, mapped to 0x8000-0x9fff
(snip)
7ffe-7fff (    2): unaccessed
```

### CHR-ROM CDL data
```
python cdlsummary.py -b 2 -p c smb.cdl
Start address, end address, length, description:
(addresses in hexadecimal, lengths in decimal)
0000-10ef (4336): rendered by PPU
10f0-10ff (  16): unaccessed
1100-112f (  48): rendered by PPU
1130-113f (  16): unaccessed
1140-120f ( 208): rendered by PPU
1210-121f (  16): unaccessed
1220-199f (1920): rendered by PPU
19a0-19af (  16): unaccessed
19b0-1ebf (1296): rendered by PPU
1ec0-1ff9 ( 314): read programmatically
1ffa-1fff (   6): unaccessed
```
