# cdl-summary
Reads an [FCEUX](http://www.fceux.com) Code/Data Logger file (extension `.cdl`) and prints it with repeating bytes grouped together.

## Command line arguments

Syntax: *options* *input_file*

### *options*
* `-b` *size* or `--prg-rom-banks`=*size*
  * *size* is the PRG-ROM size of *input_file* in 16-KiB (16,384-byte) banks.
  * *size* must be 1 to 255.
  * Default: half the *input_file* size, rounded up to the next power of two, but at least 16 KiB.
  * It is recommended to set this value manually (see below).
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
1. Find the iNES ROM file (extension `.nes`) that was used to create the `.cdl` file.
1. Open the `.nes` file in FCEUX.
1. Go to Help &rarr; Message Log.
1. You should see something like `PRG ROM: 2 x 16KiB` where `2` is the PRG-ROM size in 16-KiB banks.

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
python cdlsummary.py -p p --omit-unaccessed smb.cdl
Warning: PRG-ROM size not specified, guessing 32 KiB.
Start address (hexadecimal), end address (hexadecimal), length (decimal), description:
0000-0059 (   90): code, mapped to 0x8000-0x9fff
005a-0060 (    7): data, mapped to 0x8000-0x9fff
0062-0073 (   18): data, mapped to 0x8000-0x9fff
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
02e6-031c (   55): code, mapped to 0x8000-0x9fff
031d-0324 (    8): data, mapped to 0x8000-0x9fff
0325-033f (   27): code, mapped to 0x8000-0x9fff
0340-036a (   43): data, mapped to 0x8000-0x9fff
036b-038a (   32): code, mapped to 0x8000-0x9fff
038b-038d (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
038e-03a5 (   24): code, mapped to 0x8000-0x9fff
03a6-03af (   10): data (indirectly accessed), mapped to 0x8000-0x9fff
03b0-03b2 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
03b3-03bc (   10): code, mapped to 0x8000-0x9fff
03bd-03be (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
03bf-03f5 (   55): code, mapped to 0x8000-0x9fff
03f6-03f8 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
03f9-0460 (  104): code, mapped to 0x8000-0x9fff
0461-0463 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
0464-049e (   59): code, mapped to 0x8000-0x9fff
04a1-04b6 (   22): data, mapped to 0x8000-0x9fff
04b8-04c2 (   11): data, mapped to 0x8000-0x9fff
04c3-0566 (  164): code, mapped to 0x8000-0x9fff
0567-0569 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
056a-056c (    3): code, mapped to 0x8000-0x9fff
056d-058a (   30): data (indirectly accessed), mapped to 0x8000-0x9fff
058b-058d (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
058e-059a (   13): code, mapped to 0x8000-0x9fff
059b-059d (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
059e-05ba (   29): code, mapped to 0x8000-0x9fff
05bb-05be (    4): data, mapped to 0x8000-0x9fff
05bf-05c1 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
05c2-05ca (    9): code, mapped to 0x8000-0x9fff
05cb-05e2 (   24): data, mapped to 0x8000-0x9fff
05e3-05e5 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
05e6-0642 (   93): code, mapped to 0x8000-0x9fff
0643-0645 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
0646-0651 (   12): code, mapped to 0x8000-0x9fff
0652-0653 (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
0654-0659 (    6): code, mapped to 0x8000-0x9fff
065a-065c (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
065d-0692 (   54): code, mapped to 0x8000-0x9fff
0693-0695 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
0696-06a7 (   18): code, mapped to 0x8000-0x9fff
06a8-06aa (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
06ab-06e5 (   59): code, mapped to 0x8000-0x9fff
06e6-06e8 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
06e9-06fe (   22): code, mapped to 0x8000-0x9fff
06ff-0701 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
0702-0731 (   48): code, mapped to 0x8000-0x9fff
0732-0734 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
0735-0748 (   20): code, mapped to 0x8000-0x9fff
0749-074a (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
074b-0751 (    7): code, mapped to 0x8000-0x9fff
0752-07f4 (  163): data, mapped to 0x8000-0x9fff
07f6-07f8 (    3): data, mapped to 0x8000-0x9fff
07fa-07fc (    3): data, mapped to 0x8000-0x9fff
07fe-07fe (    1): data, mapped to 0x8000-0x9fff
0800-0800 (    1): data, mapped to 0x8000-0x9fff
0802-0807 (    6): data, mapped to 0x8000-0x9fff
0808-089c (  149): code, mapped to 0x8000-0x9fff
089d-089f (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
08a0-08ad (   14): code, mapped to 0x8000-0x9fff
08ae-08b0 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
08b1-09c2 (  274): code, mapped to 0x8000-0x9fff
09c3-09e0 (   30): data, mapped to 0x8000-0x9fff
09e1-0a38 (   88): code, mapped to 0x8000-0x9fff
0a39-0a4c (   20): data, mapped to 0x8000-0x9fff
0a4d-0b07 (  187): code, mapped to 0x8000-0x9fff
0b08-0b0f (    8): data, mapped to 0x8000-0x9fff
0b10-0b13 (    4): data (indirectly accessed), mapped to 0x8000-0x9fff
0b18-0b9b (  132): data (indirectly accessed), mapped to 0x8000-0x9fff
0ba0-0ba7 (    8): data (indirectly accessed), mapped to 0x8000-0x9fff
0bac-0bf7 (   76): data (indirectly accessed), mapped to 0x8000-0x9fff
0bfc-0c53 (   88): data (indirectly accessed), mapped to 0x8000-0x9fff
0c58-0c5f (    8): data (indirectly accessed), mapped to 0x8000-0x9fff
0c64-0e03 (  416): data (indirectly accessed), mapped to 0x8000-0x9fff
0e04-0ef3 (  240): code, mapped to 0x8000-0x9fff
0ef4-0f05 (   18): data, mapped to 0x8000-0x9fff
0f06-0fbb (  182): code, mapped to 0x8000-0x9fff
0fbc-0fce (   19): data, mapped to 0x8000-0x9fff
0fcf-0fd0 (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
0fd1-1060 (  144): code, mapped to 0x8000-0x9fff
1061-1062 (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
1063-10e6 (  132): code, mapped to 0x8000-0x9fff
10e7-10ec (    6): data, mapped to 0x8000-0x9fff
10ed-1115 (   41): code, mapped to 0x8000-0x9fff
1116-111f (   10): data, mapped to 0x8000-0x9fff
1123-1128 (    6): data, mapped to 0x8000-0x9fff
112c-112f (    4): data, mapped to 0x8000-0x9fff
1131-1133 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1134-11bc (  137): code, mapped to 0x8000-0x9fff
11bd-11cc (   16): data, mapped to 0x8000-0x9fff
11cd-11cf (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
11d0-1217 (   72): code, mapped to 0x8000-0x9fff
1218-121a (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
121b-121d (    3): code, mapped to 0x8000-0x9fff
121e-1223 (    6): data (indirectly accessed), mapped to 0x8000-0x9fff
1224-1225 (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
1226-1236 (   17): code, mapped to 0x8000-0x9fff
1237-1238 (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
1239-12ca (  146): code, mapped to 0x8000-0x9fff
12cb-12da (   16): data (indirectly accessed), mapped to 0x8000-0x9fff
12db-12dd (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
12de-12f6 (   25): code, mapped to 0x8000-0x9fff
12f7-1393 (  157): data, mapped to 0x8000-0x9fff
1396-1396 (    1): data, mapped to 0x8000-0x9fff
1399-1399 (    1): data, mapped to 0x8000-0x9fff
139c-13a5 (   10): data, mapped to 0x8000-0x9fff
13a8-13ac (    5): data, mapped to 0x8000-0x9fff
13ae-13f3 (   70): data, mapped to 0x8000-0x9fff
13f6-13fb (    6): data, mapped to 0x8000-0x9fff
13fc-13fe (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
13ff-1503 (  261): code, mapped to 0x8000-0x9fff
1504-1507 (    4): data, mapped to 0x8000-0x9fff
1508-1666 (  351): code, mapped to 0x8000-0x9fff
1667-1690 (   42): data (indirectly accessed), mapped to 0x8000-0x9fff
1693-16b6 (   36): data (indirectly accessed), mapped to 0x8000-0x9fff
16b9-16c4 (   12): data (indirectly accessed), mapped to 0x8000-0x9fff
16c5-16c7 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
16c8-16f1 (   42): code, mapped to 0x8000-0x9fff
16f2-16f3 (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
16f4-170c (   25): code, mapped to 0x8000-0x9fff
170d-170f (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1710-1727 (   24): code, mapped to 0x8000-0x9fff
1728-172a (    3): data, mapped to 0x8000-0x9fff
172b-172c (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
172d-173f (   19): code, mapped to 0x8000-0x9fff
1740-1742 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1743-1745 (    3): code, mapped to 0x8000-0x9fff
1746-174b (    6): data (indirectly accessed), mapped to 0x8000-0x9fff
174c-174e (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
174f-1777 (   41): code, mapped to 0x8000-0x9fff
1778-177a (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
177b-17b6 (   60): code, mapped to 0x8000-0x9fff
17b7-17b9 (    3): data, mapped to 0x8000-0x9fff
17ba-17bc (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
17bd-17ce (   18): code, mapped to 0x8000-0x9fff
17cf-1805 (   55): data, mapped to 0x8000-0x9fff
1806-1808 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1809-186e (  102): code, mapped to 0x8000-0x9fff
186f-1871 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1872-1881 (   16): code, mapped to 0x8000-0x9fff
1882-1883 (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
1884-189e (   27): code, mapped to 0x8000-0x9fff
189f-18aa (   12): data, mapped to 0x8000-0x9fff
18ab-18ac (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
18ad-18dc (   48): code, mapped to 0x8000-0x9fff
18dd-18e4 (    8): data, mapped to 0x8000-0x9fff
18e5-18e7 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
18e8-1956 (  111): code, mapped to 0x8000-0x9fff
1957-1959 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
195a-1967 (   14): code, mapped to 0x8000-0x9fff
1968-1969 (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
196a-1978 (   15): code, mapped to 0x8000-0x9fff
1979-197a (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
197b-197b (    1): code, mapped to 0x8000-0x9fff
197c-197d (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
197e-1993 (   22): code, mapped to 0x8000-0x9fff
199e-199f (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
19a0-19cf (   48): code, mapped to 0x8000-0x9fff
19d0-19d1 (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
19d2-19d6 (    5): code, mapped to 0x8000-0x9fff
19d7-19d7 (    1): code (indirectly accessed), mapped to 0x8000-0x9fff
19d8-19ed (   22): code, mapped to 0x8000-0x9fff
19ee-19f1 (    4): data, mapped to 0x8000-0x9fff
19f2-19f4 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
19f5-19fa (    6): code, mapped to 0x8000-0x9fff
19fb-1a00 (    6): data, mapped to 0x8000-0x9fff
1a01-1a02 (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
1a03-1a08 (    6): code, mapped to 0x8000-0x9fff
1a09-1a0a (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
1a0b-1a18 (   14): code, mapped to 0x8000-0x9fff
1a19-1a1b (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1a1c-1a24 (    9): code, mapped to 0x8000-0x9fff
1a25-1a2d (    9): data, mapped to 0x8000-0x9fff
1a2e-1a30 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1a31-1a3d (   13): code, mapped to 0x8000-0x9fff
1a3e-1a40 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1a41-1a4f (   15): code, mapped to 0x8000-0x9fff
1a50-1a52 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1a53-1a58 (    6): code, mapped to 0x8000-0x9fff
1a59-1a5b (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1a5c-1a68 (   13): code, mapped to 0x8000-0x9fff
1a69-1a6b (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1a6c-1aa4 (   57): code, mapped to 0x8000-0x9fff
1aa5-1ab6 (   18): data, mapped to 0x8000-0x9fff
1ab7-1ab9 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1aba-1ad2 (   25): code, mapped to 0x8000-0x9fff
1ad3-1ad5 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1ad6-1b00 (   43): code, mapped to 0x8000-0x9fff
1b01-1b03 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1b04-1b0d (   10): code, mapped to 0x8000-0x9fff
1b0e-1b10 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1b11-1b13 (    3): code, mapped to 0x8000-0x9fff
1b14-1b15 (    2): code (indirectly accessed), mapped to 0x8000-0x9fff
1b16-1b3c (   39): code, mapped to 0x8000-0x9fff
1b3d-1b40 (    4): data, mapped to 0x8000-0x9fff
1b41-1b43 (    3): code (indirectly accessed), mapped to 0x8000-0x9fff
1b44-1b6d (   42): code, mapped to 0x8000-0x9fff
1b70-1bdc (  109): code, mapped to 0x8000-0x9fff
1bdd-1be0 (    4): data, mapped to 0x8000-0x9fff
1be1-1bf5 (   21): code, mapped to 0x8000-0x9fff
1bf8-1bf9 (    2): data, mapped to 0x8000-0x9fff
1bfc-1bfc (    1): data, mapped to 0x8000-0x9fff
1bff-1c02 (    4): data, mapped to 0x8000-0x9fff
1c03-1cb3 (  177): code, mapped to 0x8000-0x9fff
1cb4-1d6f (  188): data, mapped to 0x8000-0x9fff
1d70-1d95 (   38): data (indirectly accessed), mapped to 0x8000-0x9fff
1d97-1dae (   24): data (indirectly accessed), mapped to 0x8000-0x9fff
1db0-1ddd (   46): data (indirectly accessed), mapped to 0x8000-0x9fff
1ddf-1e08 (   42): data (indirectly accessed), mapped to 0x8000-0x9fff
1e0a-1e1d (   20): data (indirectly accessed), mapped to 0x8000-0x9fff
1e1f-1e57 (   57): data (indirectly accessed), mapped to 0x8000-0x9fff
1e59-1fff (  423): data (indirectly accessed), mapped to 0x8000-0x9fff
2000-2eda ( 3803): data (indirectly accessed), mapped to 0xa000-0xbfff
2edc-2ede (    3): code (indirectly accessed), mapped to 0xa000-0xbfff
2edf-2ee1 (    3): code, mapped to 0xa000-0xbfff
2ee2-2ee9 (    8): data (indirectly accessed), mapped to 0xa000-0xbfff
2eea-3033 (  330): code, mapped to 0xa000-0xbfff
3034-3037 (    4): data, mapped to 0xa000-0xbfff
3038-304e (   23): code, mapped to 0xa000-0xbfff
304f-3068 (   26): data (indirectly accessed), mapped to 0xa000-0xbfff
3069-306b (    3): code (indirectly accessed), mapped to 0xa000-0xbfff
306c-30e8 (  125): code, mapped to 0xa000-0xbfff
30e9-30ea (    2): code (indirectly accessed), mapped to 0xa000-0xbfff
30eb-31c6 (  220): code, mapped to 0xa000-0xbfff
31c7-31c8 (    2): code (indirectly accessed), mapped to 0xa000-0xbfff
31c9-31e4 (   28): code, mapped to 0xa000-0xbfff
31e5-31e6 (    2): code (indirectly accessed), mapped to 0xa000-0xbfff
31e7-3205 (   31): code, mapped to 0xa000-0xbfff
3206-3208 (    3): code (indirectly accessed), mapped to 0xa000-0xbfff
3209-3232 (   42): code, mapped to 0xa000-0xbfff
3233-3235 (    3): code (indirectly accessed), mapped to 0xa000-0xbfff
3236-3244 (   15): code, mapped to 0xa000-0xbfff
3245-3247 (    3): code (indirectly accessed), mapped to 0xa000-0xbfff
3248-3268 (   33): code, mapped to 0xa000-0xbfff
3269-326b (    3): code (indirectly accessed), mapped to 0xa000-0xbfff
326c-327c (   17): code, mapped to 0xa000-0xbfff
327d-327f (    3): code (indirectly accessed), mapped to 0xa000-0xbfff
3280-32a3 (   36): code, mapped to 0xa000-0xbfff
32a4-32a5 (    2): code (indirectly accessed), mapped to 0xa000-0xbfff
32a6-32be (   25): code, mapped to 0xa000-0xbfff
32c2-32c9 (    8): data, mapped to 0xa000-0xbfff
32ca-32cb (    2): code (indirectly accessed), mapped to 0xa000-0xbfff
32cc-3350 (  133): code, mapped to 0xa000-0xbfff
3351-3358 (    8): data (indirectly accessed), mapped to 0xa000-0xbfff
3359-3359 (    1): code, mapped to 0xa000-0xbfff
335a-335c (    3): code (indirectly accessed), mapped to 0xa000-0xbfff
335d-336c (   16): code, mapped to 0xa000-0xbfff
336d-336f (    3): code (indirectly accessed), mapped to 0xa000-0xbfff
3370-3375 (    6): code, mapped to 0xa000-0xbfff
3376-3377 (    2): code (indirectly accessed), mapped to 0xa000-0xbfff
3378-33c6 (   79): code, mapped to 0xa000-0xbfff
33c7-33c8 (    2): data, mapped to 0xa000-0xbfff
33ca-33cc (    3): data, mapped to 0xa000-0xbfff
33ce-33ce (    1): data, mapped to 0xa000-0xbfff
33cf-33d1 (    3): code (indirectly accessed), mapped to 0xa000-0xbfff
33d2-3423 (   82): code, mapped to 0xa000-0xbfff
3424-344f (   44): data, mapped to 0xa000-0xbfff
3450-358b (  316): code, mapped to 0xa000-0xbfff
358c-358e (    3): data, mapped to 0xa000-0xbfff
358f-3686 (  248): code, mapped to 0xa000-0xbfff
3687-3688 (    2): data, mapped to 0xa000-0xbfff
3689-3689 (    1): code, data, mapped to 0xa000-0xbfff
368a-374a (  193): code, mapped to 0xa000-0xbfff
374b-374e (    4): data, mapped to 0xa000-0xbfff
374f-3785 (   55): code, mapped to 0xa000-0xbfff
3786-3786 (    1): code, data, mapped to 0xa000-0xbfff
3787-37a3 (   29): code, mapped to 0xa000-0xbfff
37a4-37a6 (    3): code (indirectly accessed), mapped to 0xa000-0xbfff
37a7-37db (   53): code, mapped to 0xa000-0xbfff
37dc-37dc (    1): code, data, mapped to 0xa000-0xbfff
37dd-37dd (    1): code, mapped to 0xa000-0xbfff
37de-37de (    1): code, data, mapped to 0xa000-0xbfff
37df-384a (  108): code, mapped to 0xa000-0xbfff
384b-3854 (   10): data, mapped to 0xa000-0xbfff
3855-38b5 (   97): code, mapped to 0xa000-0xbfff
38b6-38b9 (    4): data, mapped to 0xa000-0xbfff
38ba-38bc (    3): code (indirectly accessed), mapped to 0xa000-0xbfff
38bd-3948 (  140): code, mapped to 0xa000-0xbfff
3949-394a (    2): data, mapped to 0xa000-0xbfff
394b-394c (    2): code (indirectly accessed), mapped to 0xa000-0xbfff
394d-39b9 (  109): code, mapped to 0xa000-0xbfff
39ba-39bb (    2): data, mapped to 0xa000-0xbfff
39bc-3a30 (  117): code, mapped to 0xa000-0xbfff
3a31-3a32 (    2): data, mapped to 0xa000-0xbfff
3a33-3a88 (   86): code, mapped to 0xa000-0xbfff
3a89-3a93 (   11): data, mapped to 0xa000-0xbfff
3a94-3b37 (  164): code, mapped to 0xa000-0xbfff
3b38-3b3a (    3): code (indirectly accessed), mapped to 0xa000-0xbfff
3b3b-3bf7 (  189): code, mapped to 0xa000-0xbfff
3bf8-3bfd (    6): data, mapped to 0xa000-0xbfff
3bfe-3c84 (  135): code, mapped to 0xa000-0xbfff
3c85-3c86 (    2): code (indirectly accessed), mapped to 0xa000-0xbfff
3c87-3cea (  100): code, mapped to 0xa000-0xbfff
3ceb-3cec (    2): data, mapped to 0xa000-0xbfff
3ced-3dbf (  211): code, mapped to 0xa000-0xbfff
3dc0-3dd1 (   18): data (indirectly accessed), mapped to 0xa000-0xbfff
3dd2-3dd3 (    2): code (indirectly accessed), mapped to 0xa000-0xbfff
3dd4-3dde (   11): code, mapped to 0xa000-0xbfff
3ddf-3de0 (    2): code (indirectly accessed), mapped to 0xa000-0xbfff
3de1-3de7 (    7): code, mapped to 0xa000-0xbfff
3de8-3df5 (   14): data, mapped to 0xa000-0xbfff
3df6-3f9e (  425): code, mapped to 0xa000-0xbfff
3fa0-3fa0 (    1): data, mapped to 0xa000-0xbfff
3fa4-3fc2 (   31): code, mapped to 0xa000-0xbfff
3fc5-3fff (   59): code, mapped to 0xa000-0xbfff
4000-4035 (   54): code, mapped to 0xc000-0xdfff
4046-406a (   37): code, mapped to 0xc000-0xdfff
406b-408b (   33): data, mapped to 0xc000-0xdfff
408c-4281 (  502): code, mapped to 0xc000-0xdfff
4282-4283 (    2): data (indirectly accessed), mapped to 0xc000-0xdfff
4286-4289 (    4): data (indirectly accessed), mapped to 0xc000-0xdfff
428c-4293 (    8): data (indirectly accessed), mapped to 0xc000-0xdfff
4296-429b (    6): data (indirectly accessed), mapped to 0xc000-0xdfff
429e-42a7 (   10): data (indirectly accessed), mapped to 0xc000-0xdfff
42aa-42b3 (   10): data (indirectly accessed), mapped to 0xc000-0xdfff
42b8-42bd (    6): data (indirectly accessed), mapped to 0xc000-0xdfff
42c0-42c1 (    2): data (indirectly accessed), mapped to 0xc000-0xdfff
42ca-42dd (   20): data (indirectly accessed), mapped to 0xc000-0xdfff
42e0-42e1 (    2): data (indirectly accessed), mapped to 0xc000-0xdfff
42ea-42ed (    4): data (indirectly accessed), mapped to 0xc000-0xdfff
42f0-42f3 (    4): code (indirectly accessed), mapped to 0xc000-0xdfff
42f4-42f6 (    3): code, mapped to 0xc000-0xdfff
42f7-42f8 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
42f9-4306 (   14): code, mapped to 0xc000-0xdfff
4307-4308 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
4309-430b (    3): code, mapped to 0xc000-0xdfff
430c-430d (    2): data, mapped to 0xc000-0xdfff
430e-431d (   16): code, mapped to 0xc000-0xdfff
431e-4320 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
4321-4325 (    5): code, mapped to 0xc000-0xdfff
4326-4327 (    2): data, mapped to 0xc000-0xdfff
4328-4329 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
432a-4341 (   24): code, mapped to 0xc000-0xdfff
4342-4343 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
4344-4349 (    6): code, mapped to 0xc000-0xdfff
434a-434b (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
434c-4352 (    7): code, mapped to 0xc000-0xdfff
4355-436a (   22): code, mapped to 0xc000-0xdfff
436b-436c (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
436d-4374 (    8): code, mapped to 0xc000-0xdfff
4375-4377 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
4378-4384 (   13): code, mapped to 0xc000-0xdfff
4385-4387 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
4388-4397 (   16): code, mapped to 0xc000-0xdfff
4398-43a3 (   12): data, mapped to 0xc000-0xdfff
43a4-43a6 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
43a7-43cd (   39): code, mapped to 0xc000-0xdfff
43d3-444e (  124): code, mapped to 0xc000-0xdfff
444f-4451 (    3): data, mapped to 0xc000-0xdfff
4453-4456 (    4): data, mapped to 0xc000-0xdfff
4458-4458 (    1): data, mapped to 0xc000-0xdfff
4459-445d (    5): code (indirectly accessed), mapped to 0xc000-0xdfff
445e-4487 (   42): code, mapped to 0xc000-0xdfff
4488-4488 (    1): data, mapped to 0xc000-0xdfff
448b-4493 (    9): data, mapped to 0xc000-0xdfff
4499-44a7 (   15): data, mapped to 0xc000-0xdfff
44a8-44aa (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
44ab-4548 (  158): code, mapped to 0xc000-0xdfff
4549-454b (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
454c-459c (   81): code, mapped to 0xc000-0xdfff
459d-45a2 (    6): data, mapped to 0xc000-0xdfff
45a3-45a5 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
45a6-4630 (  139): code, mapped to 0xc000-0xdfff
4631-463c (   12): data, mapped to 0xc000-0xdfff
463d-463f (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
4640-4689 (   74): code, mapped to 0xc000-0xdfff
468a-469b (   18): data, mapped to 0xc000-0xdfff
469c-469e (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
469f-479f (  257): code, mapped to 0xc000-0xdfff
47a0-47a1 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
47a2-47aa (    9): code, mapped to 0xc000-0xdfff
47ab-47ac (    2): data (indirectly accessed), mapped to 0xc000-0xdfff
47af-47b6 (    8): data (indirectly accessed), mapped to 0xc000-0xdfff
47b8-47b9 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
47ba-47d0 (   23): code, mapped to 0xc000-0xdfff
47d1-47d2 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
47d3-47de (   12): code, mapped to 0xc000-0xdfff
47df-47e0 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
47e1-4802 (   34): code, mapped to 0xc000-0xdfff
4803-4804 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
4805-480a (    6): code, mapped to 0xc000-0xdfff
480b-480c (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
480d-4811 (    5): code, mapped to 0xc000-0xdfff
4812-4813 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
4814-483e (   43): code, mapped to 0xc000-0xdfff
483f-4841 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
4842-4844 (    3): code, mapped to 0xc000-0xdfff
4845-4847 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
4848-486a (   35): code, mapped to 0xc000-0xdfff
486b-4870 (    6): data, mapped to 0xc000-0xdfff
4871-4880 (   16): code, mapped to 0xc000-0xdfff
4882-4891 (   16): code, mapped to 0xc000-0xdfff
4892-4899 (    8): data (indirectly accessed), mapped to 0xc000-0xdfff
48a0-48a5 (    6): data (indirectly accessed), mapped to 0xc000-0xdfff
48a8-48a9 (    2): data (indirectly accessed), mapped to 0xc000-0xdfff
48b2-48d5 (   36): data (indirectly accessed), mapped to 0xc000-0xdfff
48d6-48d6 (    1): code (indirectly accessed), mapped to 0xc000-0xdfff
48d7-48df (    9): code, mapped to 0xc000-0xdfff
48e0-48e1 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
48e2-4909 (   40): code, mapped to 0xc000-0xdfff
490a-4911 (    8): data (indirectly accessed), mapped to 0xc000-0xdfff
4914-491b (    8): data (indirectly accessed), mapped to 0xc000-0xdfff
491e-492f (   18): data (indirectly accessed), mapped to 0xc000-0xdfff
4932-4933 (    2): data (indirectly accessed), mapped to 0xc000-0xdfff
4935-4937 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
4938-4946 (   15): code, mapped to 0xc000-0xdfff
4947-4949 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
494a-494c (    3): code, mapped to 0xc000-0xdfff
494d-494f (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
4950-4964 (   21): code, mapped to 0xc000-0xdfff
4965-4967 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
4968-4989 (   34): code, mapped to 0xc000-0xdfff
498a-4997 (   14): data (indirectly accessed), mapped to 0xc000-0xdfff
4998-49af (   24): code, mapped to 0xc000-0xdfff
49b0-49b2 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
49b3-49cd (   27): code, mapped to 0xc000-0xdfff
49ce-49d7 (   10): data, mapped to 0xc000-0xdfff
49d8-49d9 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
49da-4a0f (   54): code, mapped to 0xc000-0xdfff
4a10-4a11 (    2): data, mapped to 0xc000-0xdfff
4a12-4a70 (   95): code, mapped to 0xc000-0xdfff
4a75-4a76 (    2): code, mapped to 0xc000-0xdfff
4a77-4a78 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
4a79-4afe (  134): code, mapped to 0xc000-0xdfff
4aff-4b00 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
4b01-4b24 (   36): code, mapped to 0xc000-0xdfff
4b25-4b27 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
4b28-4b86 (   95): code, mapped to 0xc000-0xdfff
4b87-4b88 (    2): data, mapped to 0xc000-0xdfff
4b89-4b8a (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
4b8b-4c35 (  171): code, mapped to 0xc000-0xdfff
4c36-4c37 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
4c38-4c45 (   14): code, mapped to 0xc000-0xdfff
4c46-4c47 (    2): data, mapped to 0xc000-0xdfff
4c4a-4c4b (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
4c4c-4cc6 (  123): code, mapped to 0xc000-0xdfff
4cc7-4d3b (  117): data, mapped to 0xc000-0xdfff
4d3c-4d49 (   14): code, data, mapped to 0xc000-0xdfff
4d4a-4ed4 (  395): code, mapped to 0xc000-0xdfff
4ed5-4ede (   10): data, mapped to 0xc000-0xdfff
4edf-4ee0 (    2): code (indirectly accessed), data, mapped to 0xc000-0xdfff
4ee1-4ee9 (    9): code, data, mapped to 0xc000-0xdfff
4eea-4f24 (   59): code, mapped to 0xc000-0xdfff
4f25-4f27 (    3): data, mapped to 0xc000-0xdfff
4f28-4f29 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
4f2a-4fb4 (  139): code, mapped to 0xc000-0xdfff
4fb5-4fb5 (    1): code, data, mapped to 0xc000-0xdfff
4fb6-4fdc (   39): code, mapped to 0xc000-0xdfff
4fdd-4feb (   15): data, mapped to 0xc000-0xdfff
4fec-4fee (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
4fef-5060 (  114): code, mapped to 0xc000-0xdfff
5061-5064 (    4): data, mapped to 0xc000-0xdfff
5065-5066 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
5067-51d0 (  362): code, mapped to 0xc000-0xdfff
51d1-51d8 (    8): data, mapped to 0xc000-0xdfff
51d9-5294 (  188): code, mapped to 0xc000-0xdfff
5295-5296 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
5297-52cc (   54): code, mapped to 0xc000-0xdfff
52cd-52d8 (   12): data, mapped to 0xc000-0xdfff
52d9-52da (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
52db-52e7 (   13): code, mapped to 0xc000-0xdfff
52e8-52f1 (   10): data (indirectly accessed), mapped to 0xc000-0xdfff
52f2-52f3 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
52f4-5310 (   29): code, mapped to 0xc000-0xdfff
5311-5314 (    4): code (indirectly accessed), mapped to 0xc000-0xdfff
5315-534d (   57): code, mapped to 0xc000-0xdfff
534e-534f (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
5350-53a1 (   82): code, mapped to 0xc000-0xdfff
53a2-53a4 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
53a5-53af (   11): code, mapped to 0xc000-0xdfff
53b0-53b1 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
53b2-5431 (  128): code, mapped to 0xc000-0xdfff
5432-5433 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
5434-5452 (   31): code, mapped to 0xc000-0xdfff
545f-546a (   12): code, mapped to 0xc000-0xdfff
5474-5590 (  285): code, mapped to 0xc000-0xdfff
5597-55d2 (   60): code, mapped to 0xc000-0xdfff
55d3-55d4 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
55d5-5606 (   50): code, mapped to 0xc000-0xdfff
5607-5608 (    2): code (indirectly accessed), mapped to 0xc000-0xdfff
5609-5630 (   40): code, mapped to 0xc000-0xdfff
5631-5633 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
5634-563c (    9): code, mapped to 0xc000-0xdfff
563d-563f (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
5640-564e (   15): code, mapped to 0xc000-0xdfff
564f-5651 (    3): code (indirectly accessed), mapped to 0xc000-0xdfff
5652-56d5 (  132): code, mapped to 0xc000-0xdfff
56d9-5735 (   93): code, mapped to 0xc000-0xdfff
5736-573d (    8): data, mapped to 0xc000-0xdfff
573e-584c (  271): code, mapped to 0xc000-0xdfff
584f-5852 (    4): data, mapped to 0xc000-0xdfff
5853-5891 (   63): code, mapped to 0xc000-0xdfff
5892-5892 (    1): data, mapped to 0xc000-0xdfff
5895-5964 (  208): code, mapped to 0xc000-0xdfff
5965-5967 (    3): data, mapped to 0xc000-0xdfff
5969-59d1 (  105): code, mapped to 0xc000-0xdfff
59d2-59d3 (    2): data, mapped to 0xc000-0xdfff
59d4-5a24 (   81): code, mapped to 0xc000-0xdfff
5a26-5a29 (    4): data, mapped to 0xc000-0xdfff
5a2d-5a31 (    5): data, mapped to 0xc000-0xdfff
5a33-5c16 (  484): code, mapped to 0xc000-0xdfff
5c17-5c18 (    2): data, mapped to 0xc000-0xdfff
5c19-5c61 (   73): code, mapped to 0xc000-0xdfff
5c62-5c63 (    2): data, mapped to 0xc000-0xdfff
5c64-5e02 (  415): code, mapped to 0xc000-0xdfff
5e03-5e04 (    2): data, mapped to 0xc000-0xdfff
5e05-5e23 (   31): code, mapped to 0xc000-0xdfff
5e24-5e24 (    1): code, data, mapped to 0xc000-0xdfff
5e25-5e28 (    4): data, mapped to 0xc000-0xdfff
5e2a-5e2d (    4): data, mapped to 0xc000-0xdfff
5e2e-5e9c (  111): code, mapped to 0xc000-0xdfff
5ea1-5f8a (  234): code, mapped to 0xc000-0xdfff
5f8b-5f8e (    4): data, mapped to 0xc000-0xdfff
5f8f-5f95 (    7): code, mapped to 0xc000-0xdfff
5f96-5f99 (    4): data, mapped to 0xc000-0xdfff
5f9a-5fb8 (   31): code, mapped to 0xc000-0xdfff
5fb9-5fbb (    3): data, mapped to 0xc000-0xdfff
5fbd-5fc0 (    4): data, mapped to 0xc000-0xdfff
5fc1-5fff (   63): code, mapped to 0xc000-0xdfff
6000-61fc (  509): code, mapped to 0xe000-0xffff
61fd-622c (   48): data, mapped to 0xe000-0xffff
622d-6391 (  357): code, mapped to 0xe000-0xffff
639c-63ac (   17): code, mapped to 0xe000-0xffff
63ad-63c7 (   27): data, mapped to 0xe000-0xffff
63ca-63e3 (   26): data, mapped to 0xe000-0xffff
63e6-63e7 (    2): data, mapped to 0xe000-0xffff
63e8-6431 (   74): code, mapped to 0xe000-0xffff
6433-6434 (    2): data, mapped to 0xe000-0xffff
6435-64bf (  139): code, mapped to 0xe000-0xffff
64c0-64db (   28): data, mapped to 0xe000-0xffff
64dc-6540 (  101): code, mapped to 0xe000-0xffff
6541-654a (   10): data, mapped to 0xe000-0xffff
654b-6681 (  311): code, mapped to 0xe000-0xffff
6682-6685 (    4): data, mapped to 0xe000-0xffff
6686-66bd (   56): code, mapped to 0xe000-0xffff
66be-66d1 (   20): data, mapped to 0xe000-0xffff
66d2-673d (  108): code, mapped to 0xe000-0xffff
673e-683d (  256): data, mapped to 0xe000-0xffff
6840-6843 (    4): data, mapped to 0xe000-0xffff
6845-6848 (    4): data, mapped to 0xe000-0xffff
684a-6852 (    9): data, mapped to 0xe000-0xffff
6854-685e (   11): data, mapped to 0xe000-0xffff
6860-6863 (    4): data, mapped to 0xe000-0xffff
6865-686d (    9): data, mapped to 0xe000-0xffff
686f-6876 (    8): data, mapped to 0xe000-0xffff
6878-687b (    4): data, mapped to 0xe000-0xffff
687d-6bcc (  848): code, mapped to 0xe000-0xffff
6bcd-6bd0 (    4): data, mapped to 0xe000-0xffff
6bd1-6c3c (  108): code, mapped to 0xe000-0xffff
6c45-6d05 (  193): code, mapped to 0xe000-0xffff
6d06-6d08 (    3): data, mapped to 0xe000-0xffff
6d09-6e06 (  254): code, mapped to 0xe000-0xffff
6e07-6ee8 (  226): data, mapped to 0xe000-0xffff
6ee9-6f9d (  181): code, mapped to 0xe000-0xffff
6f9e-6fa3 (    6): data, mapped to 0xe000-0xffff
6fa4-709b (  248): code, mapped to 0xe000-0xffff
709c-70af (   20): data, mapped to 0xe000-0xffff
70b0-71a4 (  245): code, mapped to 0xe000-0xffff
71a5-71a7 (    3): data, mapped to 0xe000-0xffff
71a8-71e2 (   59): code, mapped to 0xe000-0xffff
71e3-71f5 (   19): data, mapped to 0xe000-0xffff
71f6-722a (   53): code, mapped to 0xe000-0xffff
722b-7232 (    8): data, mapped to 0xe000-0xffff
7234-7238 (    5): data, mapped to 0xe000-0xffff
7239-72c9 (  145): code, mapped to 0xe000-0xffff
72d0-73b0 (  225): code, mapped to 0xe000-0xffff
73b1-73be (   14): data, mapped to 0xe000-0xffff
73bf-74d3 (  277): code, mapped to 0xe000-0xffff
74d4-74f4 (   33): data, mapped to 0xe000-0xffff
74f8-7517 (   32): data, mapped to 0xe000-0xffff
7518-75bd (  166): code, mapped to 0xe000-0xffff
75c1-762a (  106): code, mapped to 0xe000-0xffff
762b-763a (   16): data, mapped to 0xe000-0xffff
763b-790c (  722): code, mapped to 0xe000-0xffff
790d-7910 (    4): data, mapped to 0xe000-0xffff
7912-7914 (    3): data, mapped to 0xe000-0xffff
7916-794e (   57): data, mapped to 0xe000-0xffff
7953-79b7 (  101): data, mapped to 0xe000-0xffff
79b8-7b23 (  364): data (indirectly accessed), mapped to 0xe000-0xffff
7b25-7ceb (  455): data (indirectly accessed), mapped to 0xe000-0xffff
7ced-7efc (  528): data (indirectly accessed), mapped to 0xe000-0xffff
7f02-7f03 (    2): data, mapped to 0xe000-0xffff
7f05-7f67 (   99): data, mapped to 0xe000-0xffff
7f69-7f6a (    2): data, mapped to 0xe000-0xffff
7f6e-7f75 (    8): data, mapped to 0xe000-0xffff
7f77-7f86 (   16): data, mapped to 0xe000-0xffff
7f88-7f8d (    6): data, mapped to 0xe000-0xffff
7f90-7f94 (    5): data, mapped to 0xe000-0xffff
7f96-7ffd (  104): data, mapped to 0xe000-0xffff
```

### CHR-ROM CDL data
```
python cdlsummary.py -p c --omit-unaccessed smb.cdl
Warning: PRG-ROM size not specified, guessing 32 KiB.
Start address (hexadecimal), end address (hexadecimal), length (decimal), description:
0000-10ef (4336): rendered
1100-112f (  48): rendered
1140-120f ( 208): rendered
1220-199f (1920): rendered
19b0-1ebf (1296): rendered
1ec0-1ff9 ( 314): read programmatically
```
