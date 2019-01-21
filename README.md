# cdl-summary
Reads an [FCEUX](http://www.fceux.com) Code/Data Logger file (extension `.cdl`) and prints it with repeating bytes grouped together.

## Command line arguments

Syntax: [*options*] *input_file*

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

### *input_file*
  * The Code/Data Logger file to read.
  * The file size must be 16 KiB to 6,120 KiB and a multiple of 8 KiB.

## How to find out the PRG-ROM size of a `.cdl` file
1. Find the iNES ROM file (extension `.nes`) that was used to create the `.cdl` file.
1. Open the `.nes` file in FCEUX.
1. Go to Help &rarr; Message Log.
1. You should see something like `PRG ROM: 2 x 16KiB` where `2` is the PRG-ROM size in 16-KiB banks.

## The structure of a `.cdl` file
A `.cdl` file consists of two parts:
1. PRG-ROM log data (16 KiB to 4,080 KiB and a multiple of 16 KiB)
1. CHR-ROM log data (0 bytes to 2,040 KiB and a multiple of 8 KiB)

See the FCEUX help (Help &rarr; Help&hellip; &rarr; Debug &rarr; Code/Data Logger) for more information on the file format.

## Examples

### PRG-ROM CDL data
```
python cdlsummary.py -p p --omit-unaccessed --ignore-bank smb.cdl
Warning: PRG-ROM size not specified, guessing 32 KiB.
Start address (hexadecimal), end address (hexadecimal), length (decimal), description:
0000-0059 (   90): code
005a-0060 (    7): data
0062-0073 (   18): data
0075-0081 (   13): data
0082-0217 (  406): code
0218-021f (    8): data (indirectly accessed)
0220-0230 (   17): code
0231-0233 (    3): code (indirectly accessed)
0234-0236 (    3): code
0237-023e (    8): data (indirectly accessed)
023f-0244 (    6): data
0245-0246 (    2): code (indirectly accessed)
0247-02df (  153): code
02e6-031c (   55): code
031d-0324 (    8): data
0325-033f (   27): code
0340-036a (   43): data
036b-038a (   32): code
038b-038d (    3): code (indirectly accessed)
038e-03a5 (   24): code
03a6-03af (   10): data (indirectly accessed)
03b0-03b2 (    3): code (indirectly accessed)
03b3-03bc (   10): code
03bd-03be (    2): code (indirectly accessed)
03bf-03f5 (   55): code
03f6-03f8 (    3): code (indirectly accessed)
03f9-0460 (  104): code
0461-0463 (    3): code (indirectly accessed)
0464-049e (   59): code
04a1-04b6 (   22): data
04b8-04c2 (   11): data
04c3-0566 (  164): code
0567-0569 (    3): code (indirectly accessed)
056a-056c (    3): code
056d-058a (   30): data (indirectly accessed)
058b-058d (    3): code (indirectly accessed)
058e-059a (   13): code
059b-059d (    3): code (indirectly accessed)
059e-05ba (   29): code
05bb-05be (    4): data
05bf-05c1 (    3): code (indirectly accessed)
05c2-05ca (    9): code
05cb-05e2 (   24): data
05e3-05e5 (    3): code (indirectly accessed)
05e6-0642 (   93): code
0643-0645 (    3): code (indirectly accessed)
0646-0651 (   12): code
0652-0653 (    2): code (indirectly accessed)
0654-0659 (    6): code
065a-065c (    3): code (indirectly accessed)
065d-0692 (   54): code
0693-0695 (    3): code (indirectly accessed)
0696-06a7 (   18): code
06a8-06aa (    3): code (indirectly accessed)
06ab-06e5 (   59): code
06e6-06e8 (    3): code (indirectly accessed)
06e9-06fe (   22): code
06ff-0701 (    3): code (indirectly accessed)
0702-0731 (   48): code
0732-0734 (    3): code (indirectly accessed)
0735-0748 (   20): code
0749-074a (    2): code (indirectly accessed)
074b-0751 (    7): code
0752-07f4 (  163): data
07f6-07f8 (    3): data
07fa-07fc (    3): data
07fe-07fe (    1): data
0800-0800 (    1): data
0802-0807 (    6): data
0808-089c (  149): code
089d-089f (    3): code (indirectly accessed)
08a0-08ad (   14): code
08ae-08b0 (    3): code (indirectly accessed)
08b1-09c2 (  274): code
09c3-09e0 (   30): data
09e1-0a38 (   88): code
0a39-0a4c (   20): data
0a4d-0b07 (  187): code
0b08-0b0f (    8): data
0b10-0b13 (    4): data (indirectly accessed)
0b18-0b9b (  132): data (indirectly accessed)
0ba0-0ba7 (    8): data (indirectly accessed)
0bac-0bf7 (   76): data (indirectly accessed)
0bfc-0c53 (   88): data (indirectly accessed)
0c58-0c5f (    8): data (indirectly accessed)
0c64-0e03 (  416): data (indirectly accessed)
0e04-0ef3 (  240): code
0ef4-0f05 (   18): data
0f06-0fbb (  182): code
0fbc-0fce (   19): data
0fcf-0fd0 (    2): code (indirectly accessed)
0fd1-1060 (  144): code
1061-1062 (    2): code (indirectly accessed)
1063-10e6 (  132): code
10e7-10ec (    6): data
10ed-1115 (   41): code
1116-111f (   10): data
1123-1128 (    6): data
112c-112f (    4): data
1131-1133 (    3): code (indirectly accessed)
1134-11bc (  137): code
11bd-11cc (   16): data
11cd-11cf (    3): code (indirectly accessed)
11d0-1217 (   72): code
1218-121a (    3): code (indirectly accessed)
121b-121d (    3): code
121e-1223 (    6): data (indirectly accessed)
1224-1225 (    2): code (indirectly accessed)
1226-1236 (   17): code
1237-1238 (    2): code (indirectly accessed)
1239-12ca (  146): code
12cb-12da (   16): data (indirectly accessed)
12db-12dd (    3): code (indirectly accessed)
12de-12f6 (   25): code
12f7-1393 (  157): data
1396-1396 (    1): data
1399-1399 (    1): data
139c-13a5 (   10): data
13a8-13ac (    5): data
13ae-13f3 (   70): data
13f6-13fb (    6): data
13fc-13fe (    3): code (indirectly accessed)
13ff-1503 (  261): code
1504-1507 (    4): data
1508-1666 (  351): code
1667-1690 (   42): data (indirectly accessed)
1693-16b6 (   36): data (indirectly accessed)
16b9-16c4 (   12): data (indirectly accessed)
16c5-16c7 (    3): code (indirectly accessed)
16c8-16f1 (   42): code
16f2-16f3 (    2): code (indirectly accessed)
16f4-170c (   25): code
170d-170f (    3): code (indirectly accessed)
1710-1727 (   24): code
1728-172a (    3): data
172b-172c (    2): code (indirectly accessed)
172d-173f (   19): code
1740-1742 (    3): code (indirectly accessed)
1743-1745 (    3): code
1746-174b (    6): data (indirectly accessed)
174c-174e (    3): code (indirectly accessed)
174f-1777 (   41): code
1778-177a (    3): code (indirectly accessed)
177b-17b6 (   60): code
17b7-17b9 (    3): data
17ba-17bc (    3): code (indirectly accessed)
17bd-17ce (   18): code
17cf-1805 (   55): data
1806-1808 (    3): code (indirectly accessed)
1809-186e (  102): code
186f-1871 (    3): code (indirectly accessed)
1872-1881 (   16): code
1882-1883 (    2): code (indirectly accessed)
1884-189e (   27): code
189f-18aa (   12): data
18ab-18ac (    2): code (indirectly accessed)
18ad-18dc (   48): code
18dd-18e4 (    8): data
18e5-18e7 (    3): code (indirectly accessed)
18e8-1956 (  111): code
1957-1959 (    3): code (indirectly accessed)
195a-1967 (   14): code
1968-1969 (    2): code (indirectly accessed)
196a-1978 (   15): code
1979-197a (    2): code (indirectly accessed)
197b-197b (    1): code
197c-197d (    2): code (indirectly accessed)
197e-1993 (   22): code
199e-199f (    2): code (indirectly accessed)
19a0-19cf (   48): code
19d0-19d1 (    2): code (indirectly accessed)
19d2-19d6 (    5): code
19d7-19d7 (    1): code (indirectly accessed)
19d8-19ed (   22): code
19ee-19f1 (    4): data
19f2-19f4 (    3): code (indirectly accessed)
19f5-19fa (    6): code
19fb-1a00 (    6): data
1a01-1a02 (    2): code (indirectly accessed)
1a03-1a08 (    6): code
1a09-1a0a (    2): code (indirectly accessed)
1a0b-1a18 (   14): code
1a19-1a1b (    3): code (indirectly accessed)
1a1c-1a24 (    9): code
1a25-1a2d (    9): data
1a2e-1a30 (    3): code (indirectly accessed)
1a31-1a3d (   13): code
1a3e-1a40 (    3): code (indirectly accessed)
1a41-1a4f (   15): code
1a50-1a52 (    3): code (indirectly accessed)
1a53-1a58 (    6): code
1a59-1a5b (    3): code (indirectly accessed)
1a5c-1a68 (   13): code
1a69-1a6b (    3): code (indirectly accessed)
1a6c-1aa4 (   57): code
1aa5-1ab6 (   18): data
1ab7-1ab9 (    3): code (indirectly accessed)
1aba-1ad2 (   25): code
1ad3-1ad5 (    3): code (indirectly accessed)
1ad6-1b00 (   43): code
1b01-1b03 (    3): code (indirectly accessed)
1b04-1b0d (   10): code
1b0e-1b10 (    3): code (indirectly accessed)
1b11-1b13 (    3): code
1b14-1b15 (    2): code (indirectly accessed)
1b16-1b3c (   39): code
1b3d-1b40 (    4): data
1b41-1b43 (    3): code (indirectly accessed)
1b44-1b6d (   42): code
1b70-1bdc (  109): code
1bdd-1be0 (    4): data
1be1-1bf5 (   21): code
1bf8-1bf9 (    2): data
1bfc-1bfc (    1): data
1bff-1c02 (    4): data
1c03-1cb3 (  177): code
1cb4-1d6f (  188): data
1d70-1d95 (   38): data (indirectly accessed)
1d97-1dae (   24): data (indirectly accessed)
1db0-1ddd (   46): data (indirectly accessed)
1ddf-1e08 (   42): data (indirectly accessed)
1e0a-1e1d (   20): data (indirectly accessed)
1e1f-1e57 (   57): data (indirectly accessed)
1e59-2eda ( 4226): data (indirectly accessed)
2edc-2ede (    3): code (indirectly accessed)
2edf-2ee1 (    3): code
2ee2-2ee9 (    8): data (indirectly accessed)
2eea-3033 (  330): code
3034-3037 (    4): data
3038-304e (   23): code
304f-3068 (   26): data (indirectly accessed)
3069-306b (    3): code (indirectly accessed)
306c-30e8 (  125): code
30e9-30ea (    2): code (indirectly accessed)
30eb-31c6 (  220): code
31c7-31c8 (    2): code (indirectly accessed)
31c9-31e4 (   28): code
31e5-31e6 (    2): code (indirectly accessed)
31e7-3205 (   31): code
3206-3208 (    3): code (indirectly accessed)
3209-3232 (   42): code
3233-3235 (    3): code (indirectly accessed)
3236-3244 (   15): code
3245-3247 (    3): code (indirectly accessed)
3248-3268 (   33): code
3269-326b (    3): code (indirectly accessed)
326c-327c (   17): code
327d-327f (    3): code (indirectly accessed)
3280-32a3 (   36): code
32a4-32a5 (    2): code (indirectly accessed)
32a6-32be (   25): code
32c2-32c9 (    8): data
32ca-32cb (    2): code (indirectly accessed)
32cc-3350 (  133): code
3351-3358 (    8): data (indirectly accessed)
3359-3359 (    1): code
335a-335c (    3): code (indirectly accessed)
335d-336c (   16): code
336d-336f (    3): code (indirectly accessed)
3370-3375 (    6): code
3376-3377 (    2): code (indirectly accessed)
3378-33c6 (   79): code
33c7-33c8 (    2): data
33ca-33cc (    3): data
33ce-33ce (    1): data
33cf-33d1 (    3): code (indirectly accessed)
33d2-3423 (   82): code
3424-344f (   44): data
3450-358b (  316): code
358c-358e (    3): data
358f-3686 (  248): code
3687-3688 (    2): data
3689-3689 (    1): code, data
368a-374a (  193): code
374b-374e (    4): data
374f-3785 (   55): code
3786-3786 (    1): code, data
3787-37a3 (   29): code
37a4-37a6 (    3): code (indirectly accessed)
37a7-37db (   53): code
37dc-37dc (    1): code, data
37dd-37dd (    1): code
37de-37de (    1): code, data
37df-384a (  108): code
384b-3854 (   10): data
3855-38b5 (   97): code
38b6-38b9 (    4): data
38ba-38bc (    3): code (indirectly accessed)
38bd-3948 (  140): code
3949-394a (    2): data
394b-394c (    2): code (indirectly accessed)
394d-39b9 (  109): code
39ba-39bb (    2): data
39bc-3a30 (  117): code
3a31-3a32 (    2): data
3a33-3a88 (   86): code
3a89-3a93 (   11): data
3a94-3b37 (  164): code
3b38-3b3a (    3): code (indirectly accessed)
3b3b-3bf7 (  189): code
3bf8-3bfd (    6): data
3bfe-3c84 (  135): code
3c85-3c86 (    2): code (indirectly accessed)
3c87-3cea (  100): code
3ceb-3cec (    2): data
3ced-3dbf (  211): code
3dc0-3dd1 (   18): data (indirectly accessed)
3dd2-3dd3 (    2): code (indirectly accessed)
3dd4-3dde (   11): code
3ddf-3de0 (    2): code (indirectly accessed)
3de1-3de7 (    7): code
3de8-3df5 (   14): data
3df6-3f9e (  425): code
3fa0-3fa0 (    1): data
3fa4-3fc2 (   31): code
3fc5-4035 (  113): code
4046-406a (   37): code
406b-408b (   33): data
408c-4281 (  502): code
4282-4283 (    2): data (indirectly accessed)
4286-4289 (    4): data (indirectly accessed)
428c-4293 (    8): data (indirectly accessed)
4296-429b (    6): data (indirectly accessed)
429e-42a7 (   10): data (indirectly accessed)
42aa-42b3 (   10): data (indirectly accessed)
42b8-42bd (    6): data (indirectly accessed)
42c0-42c1 (    2): data (indirectly accessed)
42ca-42dd (   20): data (indirectly accessed)
42e0-42e1 (    2): data (indirectly accessed)
42ea-42ed (    4): data (indirectly accessed)
42f0-42f3 (    4): code (indirectly accessed)
42f4-42f6 (    3): code
42f7-42f8 (    2): code (indirectly accessed)
42f9-4306 (   14): code
4307-4308 (    2): code (indirectly accessed)
4309-430b (    3): code
430c-430d (    2): data
430e-431d (   16): code
431e-4320 (    3): code (indirectly accessed)
4321-4325 (    5): code
4326-4327 (    2): data
4328-4329 (    2): code (indirectly accessed)
432a-4341 (   24): code
4342-4343 (    2): code (indirectly accessed)
4344-4349 (    6): code
434a-434b (    2): code (indirectly accessed)
434c-4352 (    7): code
4355-436a (   22): code
436b-436c (    2): code (indirectly accessed)
436d-4374 (    8): code
4375-4377 (    3): code (indirectly accessed)
4378-4384 (   13): code
4385-4387 (    3): code (indirectly accessed)
4388-4397 (   16): code
4398-43a3 (   12): data
43a4-43a6 (    3): code (indirectly accessed)
43a7-43cd (   39): code
43d3-444e (  124): code
444f-4451 (    3): data
4453-4456 (    4): data
4458-4458 (    1): data
4459-445d (    5): code (indirectly accessed)
445e-4487 (   42): code
4488-4488 (    1): data
448b-4493 (    9): data
4499-44a7 (   15): data
44a8-44aa (    3): code (indirectly accessed)
44ab-4548 (  158): code
4549-454b (    3): code (indirectly accessed)
454c-459c (   81): code
459d-45a2 (    6): data
45a3-45a5 (    3): code (indirectly accessed)
45a6-4630 (  139): code
4631-463c (   12): data
463d-463f (    3): code (indirectly accessed)
4640-4689 (   74): code
468a-469b (   18): data
469c-469e (    3): code (indirectly accessed)
469f-479f (  257): code
47a0-47a1 (    2): code (indirectly accessed)
47a2-47aa (    9): code
47ab-47ac (    2): data (indirectly accessed)
47af-47b6 (    8): data (indirectly accessed)
47b8-47b9 (    2): code (indirectly accessed)
47ba-47d0 (   23): code
47d1-47d2 (    2): code (indirectly accessed)
47d3-47de (   12): code
47df-47e0 (    2): code (indirectly accessed)
47e1-4802 (   34): code
4803-4804 (    2): code (indirectly accessed)
4805-480a (    6): code
480b-480c (    2): code (indirectly accessed)
480d-4811 (    5): code
4812-4813 (    2): code (indirectly accessed)
4814-483e (   43): code
483f-4841 (    3): code (indirectly accessed)
4842-4844 (    3): code
4845-4847 (    3): code (indirectly accessed)
4848-486a (   35): code
486b-4870 (    6): data
4871-4880 (   16): code
4882-4891 (   16): code
4892-4899 (    8): data (indirectly accessed)
48a0-48a5 (    6): data (indirectly accessed)
48a8-48a9 (    2): data (indirectly accessed)
48b2-48d5 (   36): data (indirectly accessed)
48d6-48d6 (    1): code (indirectly accessed)
48d7-48df (    9): code
48e0-48e1 (    2): code (indirectly accessed)
48e2-4909 (   40): code
490a-4911 (    8): data (indirectly accessed)
4914-491b (    8): data (indirectly accessed)
491e-492f (   18): data (indirectly accessed)
4932-4933 (    2): data (indirectly accessed)
4935-4937 (    3): code (indirectly accessed)
4938-4946 (   15): code
4947-4949 (    3): code (indirectly accessed)
494a-494c (    3): code
494d-494f (    3): code (indirectly accessed)
4950-4964 (   21): code
4965-4967 (    3): code (indirectly accessed)
4968-4989 (   34): code
498a-4997 (   14): data (indirectly accessed)
4998-49af (   24): code
49b0-49b2 (    3): code (indirectly accessed)
49b3-49cd (   27): code
49ce-49d7 (   10): data
49d8-49d9 (    2): code (indirectly accessed)
49da-4a0f (   54): code
4a10-4a11 (    2): data
4a12-4a70 (   95): code
4a75-4a76 (    2): code
4a77-4a78 (    2): code (indirectly accessed)
4a79-4afe (  134): code
4aff-4b00 (    2): code (indirectly accessed)
4b01-4b24 (   36): code
4b25-4b27 (    3): code (indirectly accessed)
4b28-4b86 (   95): code
4b87-4b88 (    2): data
4b89-4b8a (    2): code (indirectly accessed)
4b8b-4c35 (  171): code
4c36-4c37 (    2): code (indirectly accessed)
4c38-4c45 (   14): code
4c46-4c47 (    2): data
4c4a-4c4b (    2): code (indirectly accessed)
4c4c-4cc6 (  123): code
4cc7-4d3b (  117): data
4d3c-4d49 (   14): code, data
4d4a-4ed4 (  395): code
4ed5-4ede (   10): data
4edf-4ee0 (    2): code (indirectly accessed), data
4ee1-4ee9 (    9): code, data
4eea-4f24 (   59): code
4f25-4f27 (    3): data
4f28-4f29 (    2): code (indirectly accessed)
4f2a-4fb4 (  139): code
4fb5-4fb5 (    1): code, data
4fb6-4fdc (   39): code
4fdd-4feb (   15): data
4fec-4fee (    3): code (indirectly accessed)
4fef-5060 (  114): code
5061-5064 (    4): data
5065-5066 (    2): code (indirectly accessed)
5067-51d0 (  362): code
51d1-51d8 (    8): data
51d9-5294 (  188): code
5295-5296 (    2): code (indirectly accessed)
5297-52cc (   54): code
52cd-52d8 (   12): data
52d9-52da (    2): code (indirectly accessed)
52db-52e7 (   13): code
52e8-52f1 (   10): data (indirectly accessed)
52f2-52f3 (    2): code (indirectly accessed)
52f4-5310 (   29): code
5311-5314 (    4): code (indirectly accessed)
5315-534d (   57): code
534e-534f (    2): code (indirectly accessed)
5350-53a1 (   82): code
53a2-53a4 (    3): code (indirectly accessed)
53a5-53af (   11): code
53b0-53b1 (    2): code (indirectly accessed)
53b2-5431 (  128): code
5432-5433 (    2): code (indirectly accessed)
5434-5452 (   31): code
545f-546a (   12): code
5474-5590 (  285): code
5597-55d2 (   60): code
55d3-55d4 (    2): code (indirectly accessed)
55d5-5606 (   50): code
5607-5608 (    2): code (indirectly accessed)
5609-5630 (   40): code
5631-5633 (    3): code (indirectly accessed)
5634-563c (    9): code
563d-563f (    3): code (indirectly accessed)
5640-564e (   15): code
564f-5651 (    3): code (indirectly accessed)
5652-56d5 (  132): code
56d9-5735 (   93): code
5736-573d (    8): data
573e-584c (  271): code
584f-5852 (    4): data
5853-5891 (   63): code
5892-5892 (    1): data
5895-5964 (  208): code
5965-5967 (    3): data
5969-59d1 (  105): code
59d2-59d3 (    2): data
59d4-5a24 (   81): code
5a26-5a29 (    4): data
5a2d-5a31 (    5): data
5a33-5c16 (  484): code
5c17-5c18 (    2): data
5c19-5c61 (   73): code
5c62-5c63 (    2): data
5c64-5e02 (  415): code
5e03-5e04 (    2): data
5e05-5e23 (   31): code
5e24-5e24 (    1): code, data
5e25-5e28 (    4): data
5e2a-5e2d (    4): data
5e2e-5e9c (  111): code
5ea1-5f8a (  234): code
5f8b-5f8e (    4): data
5f8f-5f95 (    7): code
5f96-5f99 (    4): data
5f9a-5fb8 (   31): code
5fb9-5fbb (    3): data
5fbd-5fc0 (    4): data
5fc1-61fc (  572): code
61fd-622c (   48): data
622d-6391 (  357): code
639c-63ac (   17): code
63ad-63c7 (   27): data
63ca-63e3 (   26): data
63e6-63e7 (    2): data
63e8-6431 (   74): code
6433-6434 (    2): data
6435-64bf (  139): code
64c0-64db (   28): data
64dc-6540 (  101): code
6541-654a (   10): data
654b-6681 (  311): code
6682-6685 (    4): data
6686-66bd (   56): code
66be-66d1 (   20): data
66d2-673d (  108): code
673e-683d (  256): data
6840-6843 (    4): data
6845-6848 (    4): data
684a-6852 (    9): data
6854-685e (   11): data
6860-6863 (    4): data
6865-686d (    9): data
686f-6876 (    8): data
6878-687b (    4): data
687d-6bcc (  848): code
6bcd-6bd0 (    4): data
6bd1-6c3c (  108): code
6c45-6d05 (  193): code
6d06-6d08 (    3): data
6d09-6e06 (  254): code
6e07-6ee8 (  226): data
6ee9-6f9d (  181): code
6f9e-6fa3 (    6): data
6fa4-709b (  248): code
709c-70af (   20): data
70b0-71a4 (  245): code
71a5-71a7 (    3): data
71a8-71e2 (   59): code
71e3-71f5 (   19): data
71f6-722a (   53): code
722b-7232 (    8): data
7234-7238 (    5): data
7239-72c9 (  145): code
72d0-73b0 (  225): code
73b1-73be (   14): data
73bf-74d3 (  277): code
74d4-74f4 (   33): data
74f8-7517 (   32): data
7518-75bd (  166): code
75c1-762a (  106): code
762b-763a (   16): data
763b-790c (  722): code
790d-7910 (    4): data
7912-7914 (    3): data
7916-794e (   57): data
7953-79b7 (  101): data
79b8-7b23 (  364): data (indirectly accessed)
7b25-7ceb (  455): data (indirectly accessed)
7ced-7efc (  528): data (indirectly accessed)
7f02-7f03 (    2): data
7f05-7f67 (   99): data
7f69-7f6a (    2): data
7f6e-7f75 (    8): data
7f77-7f86 (   16): data
7f88-7f8d (    6): data
7f90-7f94 (    5): data
7f96-7ffd (  104): data
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

## To do
* add option: origin address (default 8000 for PRG, 0000 for CHR)
* add option: bank size (default 8000 for PRG, 2000 for CHR)
