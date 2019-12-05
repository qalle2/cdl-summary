# cdl-summary
Reads an [FCEUX](http://www.fceux.com) Code/Data Logger file (extension `.cdl`) and prints it with repeating bytes grouped together.

## Command line arguments

Syntax: [*options*] *input_file*

### *options*

#### Switches
* `-m`, `--ignore-method`
  * Don't care about how bytes were accessed.
* `--ignore-directness`
  * Do not care whether PRG ROM bytes were accessed directly or indirectly.
  * Has no effect with CHR ROM or `--ignore-method`
* `--ignore-pcm`
  * Do not care whether PRG ROM bytes were accessed as PCM data.
  * Has no effect with CHR ROM or `--ignore-method`
* `--ignore-cpu-bank`
  * Do not care which CPU bank PRG ROM bytes were mapped to when last accessed.
  * Has no effect with CHR ROM or `--ignore-method`
* `-u`, `--omit-unaccessed`
  * Exclude unaccessed blocks from the output.
* `--csv`
  * Output in machine-readable format (CSV).

#### Other options
Integer arguments can be decimal (no prefix) or hexadecimal (prefix `0x`; e.g. `0x100` = 256).

* `-g` *size*, `--prg-rom-size` *size*
  * *size* is the PRG ROM size of *input_file* in 16-KiB (16,384-byte) units (e.g. 2 = 32 KiB).
  * Values:
    * minimum: 1 (or more, depending on input file size)
    * default: guessed based on the size of the input file:
	  * for 16-KiB files: 1
	  * for 4,096-KiB files: 256
	  * for files of other size: half the file size, rounded up to the next power of two (e.g. 2 (32 KiB) for files of 40&ndash;64 KiB)
    * maximum: 256 (or less, depending on input file size)
* `-p` *part*, `--part` *part*
  * Which part to read from *input_file* (case insensitive):
    * `P`: PRG ROM (the default)
    * `C`: CHR ROM
* `-r` *size*, `--rom-bank-size `*size*
  * Assume the game uses PRG/CHR ROM banks of this size.
  * *size* is the bank size.
  * The size must be a power of two.
  * Values for PRG ROM: `0x1000`, `0x2000`, `0x4000`, `0x8000` (only if the PRG ROM size is a multiple of it)
    * the maximum value is the default
  * Values for CHR ROM:, `0x1000`, `0x2000` (the default)
* `--origin` *address*
  * Assume each ROM bank starts from this CPU/PPU address.
  * Values for PRG ROM: `0x8000`, `0x9000`, `0xa000`, `0xb000`, `0xc000`, `0xd000`, `0xe000`, `0xf000`
	* not greater than `0x10000` minus the ROM bank size
	* the maximum value is the default
  * Values for CHR ROM: `0` (the default), `0x1000` (only if the ROM bank size is `0x1000`)

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
1. You should see something like `PRG ROM: 2 x 16KiB` where `2` is the PRG ROM size in 16-KiB units.

## Output
The program prints the contents of the PRG ROM or CHR ROM part of the CDL file as blocks (runs of same or similar bytes, depending on settings). Each line represents a block.

### Human-readable
All numbers are in hexadecimal.

The columns:
* `PRG`/`CHR`: PRG/CHR ROM address range (e.g. `PRG 001000-0010a3`)
* `bank`: ROM bank number (e.g. `bank 000`)
* `off`: address range within the ROM bank (e.g. `off 0000-00a3`)
* `CPU`/`PPU`: CPU/PPU address range (e.g. `CPU f000-f0a3`; equals the previous column, with the origin (here `0xf000`) added to both values)
* `len`: size of the block in bytes (e.g. `len 00a4`)
* description of the block (e.g. `code (indirectly accessed), last mapped to CPU bank 0xc000-0xdfff`)

### CSV
All numbers are in decimal.

The fields (separated by commas):
* start of the PRG/CHR ROM address range
* ROM bank number
* start of the address range within the ROM bank
* start of the CPU/PPU address range
* size of the block in bytes
* CDL byte (incorrect when using the "ignore" switches)
* description of the block in "double quotes"

## Examples

### PRG ROM
```
python cdl_summary.py cdl\excite.cdl

Guessing PRG ROM size: 1 * 16 KiB
Guessing ROM bank size: 0x4000
Guessing CPU origin address: 0xc000
PRG 000000-000007, bank 000, off 0000-0007, CPU c000-c007, len 0008: data
PRG 000008-00000f, bank 000, off 0008-000f, CPU c008-c00f, len 0008: unaccessed
PRG 000010-00001f, bank 000, off 0010-001f, CPU c010-c01f, len 0010: data
PRG 000020-000023, bank 000, off 0020-0023, CPU c020-c023, len 0004: unaccessed
PRG 000024-00002d, bank 000, off 0024-002d, CPU c024-c02d, len 000a: data
PRG 00002e-00002e, bank 000, off 002e-002e, CPU c02e-c02e, len 0001: unaccessed
PRG 00002f-000036, bank 000, off 002f-0036, CPU c02f-c036, len 0008: data
PRG 000037-000037, bank 000, off 0037-0037, CPU c037-c037, len 0001: unaccessed
PRG 000038-00003b, bank 000, off 0038-003b, CPU c038-c03b, len 0004: data
PRG 00003c-00005b, bank 000, off 003c-005b, CPU c03c-c05b, len 0020: data (indirectly accessed)
(snip)
```

### PRG ROM in CSV format
```
python cdl_summary.py --csv cdl\excite.cdl

Guessing PRG ROM size: 1 * 16 KiB
Guessing ROM bank size: 0x4000
Guessing CPU origin address: 0xc000
0,0,0,49152,8,10,"data"
8,0,8,49160,8,0,"unaccessed"
16,0,16,49168,16,10,"data"
32,0,32,49184,4,0,"unaccessed"
36,0,36,49188,10,10,"data"
46,0,46,49198,1,0,"unaccessed"
47,0,47,49199,8,10,"data"
55,0,55,49207,1,0,"unaccessed"
56,0,56,49208,4,10,"data"
60,0,60,49212,32,42,"data (indirectly accessed)"
(snip)
```

### CHR ROM
```
python cdl_summary.py --part c cdl\excite.cdl

Guessing PRG ROM size: 1 * 16 KiB
Guessing ROM bank size: 0x2000
Guessing PPU origin address: 0x0000
CHR 000000-000def, bank 000, off 0000-0def, PPU 0000-0def, len 0df0: rendered
CHR 000df0-000e0f, bank 000, off 0df0-0e0f, PPU 0df0-0e0f, len 0020: unaccessed
CHR 000e10-000fcf, bank 000, off 0e10-0fcf, PPU 0e10-0fcf, len 01c0: rendered
CHR 000fd0-000fdf, bank 000, off 0fd0-0fdf, PPU 0fd0-0fdf, len 0010: unaccessed
CHR 000fe0-00120f, bank 000, off 0fe0-120f, PPU 0fe0-120f, len 0230: rendered
CHR 001210-00121f, bank 000, off 1210-121f, PPU 1210-121f, len 0010: unaccessed
CHR 001220-00122f, bank 000, off 1220-122f, PPU 1220-122f, len 0010: rendered
CHR 001230-00123f, bank 000, off 1230-123f, PPU 1230-123f, len 0010: unaccessed
CHR 001240-00134f, bank 000, off 1240-134f, PPU 1240-134f, len 0110: rendered
CHR 001350-00135f, bank 000, off 1350-135f, PPU 1350-135f, len 0010: unaccessed
(snip)
```

### CHR ROM in CSV format
```
python cdl_summary.py --part c --csv cdl\excite.cdl

Guessing PRG ROM size: 1 * 16 KiB
Guessing ROM bank size: 0x2000
Guessing PPU origin address: 0x0000
0,0,0,0,3568,1,"rendered"
3568,0,3568,3568,32,0,"unaccessed"
3600,0,3600,3600,448,1,"rendered"
4048,0,4048,4048,16,0,"unaccessed"
4064,0,4064,4064,560,1,"rendered"
4624,0,4624,4624,16,0,"unaccessed"
4640,0,4640,4640,16,1,"rendered"
4656,0,4656,4656,16,0,"unaccessed"
4672,0,4672,4672,272,1,"rendered"
4944,0,4944,4944,16,0,"unaccessed"
(snip)
```

## References
* [FCEUX Help &ndash; Code/Data Logger](http://www.fceux.com/web/help/fceux.html?CodeDataLogger.html) (contains a description of the CDL file format)
