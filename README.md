# cdl-summary
Reads an [FCEUX](http://www.fceux.com) Code/Data Logger file (extension `.cdl`) and prints it with repeating bytes grouped together.

## Command line arguments

Syntax: [*options*] *input_file*

### *options*
Integer arguments can be decimal (no prefix) or hexadecimal (prefix `0x`; e.g. `0x100` = 256).

* `-b` *size*, `--prg-rom-banks` *size*
  * *size* is the PRG ROM size of *input_file* in 16-KiB (16,384-byte) banks.
  * *size* must be 1 to 256.
  * Default: half the *input_file* size, rounded up to the next power of two, but at least 16 KiB.
  * It is recommended to set this value manually (see below).
* `-p` *part*, `--part` *part*
  * Which part to read from *input_file* (case insensitive):
    * `P`: PRG ROM (the default)
    * `C`: CHR ROM
* `-u`, `--omit-unaccessed`
  * Exclude unaccessed blocks from the output.
* `-m`, `--ignore-method`
  * Do not care whether blocks were accessed as PCM data, nor whether they were accessed indirectly or directly.
  * Only affects the PRG ROM part.
* `-n`, `--ignore-cpu-bank`
  * Do not care which CPU bank the bytes was mapped to when last accessed.
  * Only affects the PRG ROM part.
* `-r` *size*, `--rom-bank-size `*size*
  * Assume the game uses PRG/CHR ROM banks of this size.
  * *size* is the bank size.
  * values for PRG ROM:
    * minimum: `0x100` (256)
    * default: PRG ROM size or `0x8000` (32,768), whichever is smaller
	* maximum: `0x8000` (32,768)
  * values for CHR ROM:
    * minimum: `0x100` (256)
	* default: `0x2000` (8,192)
	* maximum: `0x2000` (8,192)
* `-o` *address*, `--origin *address*
  * Assume each ROM bank starts from this CPU/PPU address.
  * values for PRG ROM:
    * minimum: `0x8000` (32,768)
    * default: `0x10000` (65,536) minus the ROM bank size
	* maximum: `0xff00` (65,280)
  * values for CHR ROM:
    * minimum: `0`
    * default: `0x2000` (8,192) minus the ROM bank size
	* maximum: `0x1f00` (7,936)
* `--csv`
  * Output in machine-readable format (CSV, decimal integers separated by commas).

Note: CPU/PPU origin address plus ROM bank size must not exceed 64 KiB for PRG ROM or 8 KiB for CHR ROM.

### *input_file*
  * The Code/Data Logger file to read.
  * File size:
    * minimum: 16 KiB
    * maximum: 6,136 KiB (256&times;16 KiB + 255&times;8 KiB)
    * a multiple of 8 KiB

## How to find out the PRG ROM size of a `.cdl` file
1. Find the iNES ROM file (extension `.nes`) that was used to create the `.cdl` file.
1. Open the `.nes` file in FCEUX.
1. Go to Help &rarr; Message Log.
1. You should see something like `PRG ROM: 2 x 16KiB` where `2` is the PRG ROM size in 16-KiB banks.

## Examples

### PRG ROM CDL data
```
python cdl_summary.py -m cdl\excite.cdl

Guessing PRG ROM bank count: 1
Guessing ROM bank size: 0x4000
Guessing CPU origin address: 0xc000
ROM bank 000, CPU address c000-c007 (length    8): data
ROM bank 000, CPU address c008-c00f (length    8): unaccessed
ROM bank 000, CPU address c010-c01f (length   10): data
ROM bank 000, CPU address c020-c023 (length    4): unaccessed
ROM bank 000, CPU address c024-c02d (length    a): data
ROM bank 000, CPU address c02e-c02e (length    1): unaccessed
ROM bank 000, CPU address c02f-c036 (length    8): data
ROM bank 000, CPU address c037-c037 (length    1): unaccessed
ROM bank 000, CPU address c038-c05b (length   24): data
ROM bank 000, CPU address c05c-c063 (length    8): unaccessed
(snip)
```

### CHR ROM CDL data
```
python cdl_summary.py --part c cdl\excite.cdl

Guessing PRG ROM bank count: 1
Guessing ROM bank size: 0x2000
Guessing PPU origin address: 0x0000
ROM bank 000, PPU address 0000-0def (length  df0): rendered
ROM bank 000, PPU address 0df0-0e0f (length   20): unaccessed
ROM bank 000, PPU address 0e10-0fcf (length  1c0): rendered
ROM bank 000, PPU address 0fd0-0fdf (length   10): unaccessed
ROM bank 000, PPU address 0fe0-120f (length  230): rendered
ROM bank 000, PPU address 1210-121f (length   10): unaccessed
ROM bank 000, PPU address 1220-122f (length   10): rendered
ROM bank 000, PPU address 1230-123f (length   10): unaccessed
ROM bank 000, PPU address 1240-134f (length  110): rendered
ROM bank 000, PPU address 1350-135f (length   10): unaccessed
(snip)
```

## References
* [FCEUX Help &ndash; Code/Data Logger](http://www.fceux.com/web/help/fceux.html?CodeDataLogger.html) (contains a description of the CDL file format)
