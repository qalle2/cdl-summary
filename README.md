# cdl-summary
Reads an [FCEUX](http://www.fceux.com) Code/Data Logger file (extension `.cdl`) and prints it with repeating bytes grouped together.

## Command line arguments

Syntax: [*options*] *input_file*

### *options*
* `-b` *size* or `--prg-rom-banks`=*size*
  * *size* is the PRG ROM size of *input_file* in 16-KiB (16,384-byte) banks.
  * *size* must be 1 to 256.
  * Default: half the *input_file* size, rounded up to the next power of two, but at least 16 KiB.
  * It is recommended to set this value manually (see below).
* `-p` *part* or `--part`=*part*
  * Which part to read from *input_file* (case insensitive):
    * `P`: PRG ROM (the default)
    * `C`: CHR ROM
* `--omit-unaccessed`
  * Exclude unaccessed bytes from the output.
* `--ignore-method`
  * Do not care whether bytes were accessed as PCM data, nor whether they were accessed indirectly or directly.
  * Only affects the PRG ROM part.
* `--ignore-cpu-bank`
  * Do not care which CPU bank the bytes were mapped to when last accessed.
  * Only affects the PRG ROM part.
* `--rom-bank-size=`*size*
  * Assume the game uses ROM banks of this size.
  * *size* is the bank size in hexadecimal.
  * If the PRG ROM part is being examined:
    * valid values: `1000`, `2000`, `4000`, `8000`
    * default value: PRG ROM size or `8000`, whichever is smaller
  * If the CHR ROM part is being examined:
    * valid values: `400`, `800`, `1000`, `2000`
    * default value: `2000`
* `--cpu-origin-address=`*address*
  * Assume each ROM bank starts from this CPU/PPU address.
  * *address* is the origin address in hexadecimal.
  * If the PRG ROM part is being examined:
    * valid values: `8000`&hellip;`fc00` and a multiple of `400`
    * default: `10000` minus the ROM bank size
  * If the CHR ROM part is being examined:
    * valid values: `0000`&hellip;`1c00` and a multiple of `400`
    * default: `0000`
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

## The structure of a `.cdl` file
A `.cdl` file consists of two parts:
1. PRG ROM log data (16 KiB to 4 MiB and a multiple of 16 KiB)
1. CHR ROM log data (optional; 8 KiB to 2,040 KiB and a multiple of 8 KiB)

See the FCEUX help (Help &rarr; Help&hellip; &rarr; Debug &rarr; Code/Data Logger) for more information on the file format.

## Examples

### PRG ROM CDL data
```
python cdl_summary.py cdl\excite.cdl

Warning: PRG ROM size not specified, guessing 16 KiB.
ROM bank 000, CPU address c000-c007, length 0008: data
ROM bank 000, CPU address c008-c00f, length 0008: unaccessed
ROM bank 000, CPU address c010-c01f, length 0010: data
ROM bank 000, CPU address c020-c023, length 0004: unaccessed
ROM bank 000, CPU address c024-c02d, length 000a: data
ROM bank 000, CPU address c02e-c02e, length 0001: unaccessed
ROM bank 000, CPU address c02f-c036, length 0008: data
ROM bank 000, CPU address c037-c037, length 0001: unaccessed
ROM bank 000, CPU address c038-c03b, length 0004: data
ROM bank 000, CPU address c03c-c05b, length 0020: data (indirectly accessed)
ROM bank 000, CPU address c05c-c063, length 0008: unaccessed
(snip)
```

### CHR ROM CDL data
```
python cdl_summary.py --part=c cdl\excite.cdl

Warning: PRG ROM size not specified, guessing 16 KiB.
ROM bank 000, CPU address 0000-0def, length 0df0: rendered
ROM bank 000, CPU address 0df0-0e0f, length 0020: unaccessed
ROM bank 000, CPU address 0e10-0fcf, length 01c0: rendered
ROM bank 000, CPU address 0fd0-0fdf, length 0010: unaccessed
ROM bank 000, CPU address 0fe0-120f, length 0230: rendered
ROM bank 000, CPU address 1210-121f, length 0010: unaccessed
ROM bank 000, CPU address 1220-122f, length 0010: rendered
ROM bank 000, CPU address 1230-123f, length 0010: unaccessed
(snip)
```

## References
* [FCEUX Help &ndash; Code/Data Logger](http://www.fceux.com/web/help/fceux.html?CodeDataLogger.html) (contains a description of the CDL file format)
