# cdl-summary

Table of contents:
* [cdl_summary.py](#cdl_summarypy)
* [cdl2png.py](#cdl2pngpy)
* [Sample CDL files](#sample-cdl-files)

## cdl_summary.py
Print an FCEUX Code/Data Logger file (.cdl) in human-readable format.

Command line arguments: *Options* *InputFile*

*Options*:
* `-r N` or `--prg-size N`: The PRG ROM size of the input file:
  * `N` is the size in kilobytes. It must be 16 to 4096 and a multiple of 16. It is usually a power of two (16, 32, 64, &hellip;).
  * This option is required.
* `-p PART` or `--part PART`: Which part to read from the input file. `PART` must be one of:
  * `p` = PRG ROM. This is the default.
  * `c` = CHR ROM.
* `-b N` or `--bank-size N`: The size of the PRG/CHR ROM banks in kilobytes:
  * For PRG ROM, `N` must be 8, 16 or 32. Default: 16 for 16-KiB PRG ROM, otherwise 32.
  * For CHR ROM, `N` must be 1, 2, 4 or 8. Default: 8.
* `-o N` or `--origin N`: The CPU/PPU address each PRG/CHR ROM bank starts from, in kilobytes:
  * For PRG ROM, `N` must be 32, 40, 48 or 56 (for addresses 0x8000, 0xa000, 0xc000 or 0xe000, respectively) but not greater than 64 minus `--bank-size`. The default is the greatest value possible.
  * For CHR ROM, `N` must be 0 to 7 but not greater than 8 minus `--bank-size`. The default is 0.
* `--ignore-access-method`: Ignore how PRG ROM bytes are accessed (directly, indirectly or as PCM audio).
* `-f FORMAT` or `--output-format FORMAT`: How to print the results. `FORMAT` must be one of:
  * `c` = CSV (fields separated by commas, all numbers in decimal, strings quoted). This is the default.
  * `t` = tabular (constant-width fields, all numbers in hexadecimal).
* `-h` or `--help`: Print a shorter version of this help and exit.

*InputFile*: The `.cdl` file to read. The size must be 16 to 6136 kilobytes and a multiple of 8 kilobytes.

### Examples

PRG ROM &ndash; CSV output:
```
$ python3 cdl_summary.py --prg-size 16 --bank-size 16 cdl/gamegenie.cdl
"ROM address","bank","offset in bank","NES address","CDL byte repeat count",
"CDL byte","CDL byte description"
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
$ python3 cdl_summary.py --prg-size 16 --bank-size 16 --output-format t
cdl/gamegenie.cdl
ROM address, bank, offset in bank, NES address, CDL byte repeat count, CDL
byte, CDL byte description (all numbers in hexadecimal):
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

## cdl2png.py
Convert an FCEUX Code/Data Logger file (.cdl) into an image file. Requires [Pillow](https://python-pillow.org).

Command line arguments: *InputFile* *OutputFile*:
* *InputFile*: The `.cdl` file to read.
* *OutputFile*: The PNG image file to write.

Each pixel in the output file corresponds to a byte in the CDL data. Colors:
* black = unaccessed
* orange = code (for PRG ROM) or rendered (for CHR ROM)
* blue = data (for PRG ROM) or read programmatically (for CHR ROM)
* white = both orange and blue.

An example from *Super Mario Bros.* by Nintendo:

![a CDL file as a PNG file](cdl2png-example.png)

There are more examples under `cdl/`.

## Sample CDL files
There are some CDL files under `cdl/`.

Percentage of unlogged bytes (lower is better):
* `blastermaster-u.cdl`: 19%
* `daysofthunder-u.cdl`: 9%
* `drmario-ju-prg0.cdl`: 14%
* `drmario-ju-prg1.cdl`: 18%
* `excitebike-ju.cdl`: 6%
* `gamegenie.cdl`: 82%
* `golf-u.cdl`: 3%
* `lunarpool-u.cdl`: 14%
* `smb1-w.cdl`: 1%
