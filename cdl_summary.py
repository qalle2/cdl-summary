import argparse, os, sys

# bitmasks for CDL data bytes; see http://fceux.com/web/help/CodeDataLogger.html
PRG_PCM_AUDIO     = 1 << 6
PRG_INDIRECT_DATA = 1 << 5
PRG_INDIRECT_CODE = 1 << 4
PRG_CPU_BANK_HI   = 1 << 3
PRG_CPU_BANK_LO   = 1 << 2
PRG_DATA          = 1 << 1
PRG_CODE          = 1 << 0
CHR_READ_PROGRAMMATICALLY = 1 << 1
CHR_RENDERED              = 1 << 0

# CSV/table headers
HEADERS = (
    "ROM address", "bank", "offset in bank", "NES address", "CDL byte repeat count", "CDL byte",
    "CDL byte description",
)

def parse_arguments():
    # parse command line arguments using argparse

    parser = argparse.ArgumentParser(
        description="Print an FCEUX Code/Data Logger file (.cdl) in human-readable format."
    )

    parser.add_argument(
        "-r", "--prg-size", type=int, required=True,
        help="PRG ROM size of input file, in KiB (16-4096 and a multiple of 16, usually a power "
        "of two). Required."
    )
    parser.add_argument(
        "-p", "--part", choices=("p", "c"), default="p",
        help="Which part to read from input file. 'p'=PRG ROM, 'c'=CHR ROM. Default='p'."
    )
    parser.add_argument(
        "-b", "--bank-size", type=int, choices=(1, 2, 4, 8, 16, 32), required=True,
        help="Size of ROM banks in KiB. 8/16/32 for PRG ROM, 1/2/4/8 for CHR ROM. Required."
    )
    parser.add_argument(
        "-o", "--origin", type=int, choices=(0, 1, 2, 3, 4, 5, 6, 7, 32, 40, 48, 56),
        help="The CPU/PPU address each ROM bank starts from, in KiB. For PRG ROM: 32/40/48/56 but "
        "not greater than 64 minus --bank-size; default=maximum. For CHR ROM: 0-7 but not greater "
        "than 8 minus --bank-size; default=0."
    )
    parser.add_argument(
        "-m", "--ignore-access-method", action="store_true",
        help="Ignore how PRG ROM bytes were accessed (directly/indirectly/as PCM audio)."
    )
    parser.add_argument(
        "-f", "--output-format", choices={"c", "t"}, default="c",
        help="Output format. 'c' = CSV (fields separated by commas, numbers in decimal, strings "
        "quoted); 't'=tabular (constant-width fields, numbers in hexadecimal). Default='c'."
    )
    parser.add_argument(
        "input_file", help="The .cdl file to read. Size: 16-6136 KiB and a multiple of 8 KiB."
    )

    args = parser.parse_args()

    # note: CDL file = data for PRG ROM (1-256 times 16 KiB) + data for CHR ROM (0-255 times 8 KiB)

    # validate PRG size, bank size and origin
    if args.prg_size % 16 or not 16 <= args.prg_size <= 256 * 16:
        sys.exit("Invalid PRG ROM size.")
    if args.part == "p" and args.bank_size < 8 or args.part == "c" and args.bank_size > 8:
        sys.exit("Invalid ROM bank size.")
    if args.part == "p" and args.prg_size % args.bank_size:
        sys.exit("PRG ROM size must be divisible by PRG ROM bank size.")
    if args.origin is not None and (
        args.part == "p" and not 32 <= args.origin <= 64 - args.bank_size
        or args.part == "c" and not 0 <= args.origin <= 8 - args.bank_size
    ):
        sys.exit("Invalid CPU/PPU origin address.")

    # validate file size against the numbers we just validated
    if not os.path.isfile(args.input_file):
        sys.exit("File not found.")
    try:
        fileSize = os.path.getsize(args.input_file)
    except OSError:
        sys.exit("Error getting file size.")
    if fileSize % (8 * 1024) or not 16 * 1024 <= fileSize <= (256 * 16 + 255 * 8) * 1024:
        sys.exit("Invalid file size.")
    if fileSize > (args.prg_size + 255 * 8) * 1024:
        sys.exit("PRG ROM is too small w.r.t. file size (CHR ROM would be too large).")
    if args.part == "c" and fileSize == args.prg_size * 1024:
        sys.exit("File has no CHR ROM.")

    return args

def get_file_info(fileSize, args):
    # get more info on what to do

    # address range
    if args.part == "p":
        partStart = 0
        partSize = args.prg_size * 1024
    else:
        partStart = args.prg_size * 1024
        partSize = fileSize - args.prg_size * 1024

    # origin
    if args.origin is not None:
        origin = args.origin * 1024
    elif args.part == "p":
        origin = (64 - args.bank_size) * 1024
    else:
        origin = 0

    # bitmask to AND all CDL bytes with
    if args.part == "p":
        bitmask = PRG_DATA | PRG_CODE
        if not args.ignore_access_method:
            bitmask |= PRG_PCM_AUDIO | PRG_INDIRECT_DATA | PRG_INDIRECT_CODE
        if args.bank_size <= 16:
            bitmask |= PRG_CPU_BANK_HI
            if args.bank_size == 8:
                bitmask |= PRG_CPU_BANK_LO
    else:
        bitmask = CHR_READ_PROGRAMMATICALLY | CHR_RENDERED

    return {
        "partStart": partStart,
        "partSize": partSize,
        "origin": origin,
        "bitmask": bitmask,
    }

def read_file_slice(handle, bytesLeft):
    # generate part of file in chunks
    while bytesLeft > 0:
        chunkSize = min(bytesLeft, 2 ** 20)
        yield handle.read(chunkSize)
        bytesLeft -= chunkSize

def generate_cdl_blocks(handle, fileInfo, args):
    # read PRG/CHR ROM from CDL file; notes: "chunk" = bufferful of unprocessed data; "block" =
    # sequence of repeating bytes; for each block, generate (rom_address, length, value)

    chunkStart = 0     # start address of current chunk
    blockStart = None  # start address of current block
    blockByte = None   # current repeating byte value

    handle.seek(fileInfo["partStart"])
    for chunk in read_file_slice(handle, fileInfo["partSize"]):
        for (pos, byte) in enumerate(chunk):
            byte &= fileInfo["bitmask"]
            if blockByte is None:
                # start new block
                blockStart = chunkStart + pos
                blockByte = byte
            elif byte != blockByte or (chunkStart + pos) % (args.bank_size * 1024) == 0:
                # end current block, start new one
                yield (blockStart, chunkStart + pos - blockStart, blockByte)
                blockStart = chunkStart + pos
                blockByte = byte
        # remember distance from the start of PRG/CHR ROM
        chunkStart += len(chunk)
    # end last block
    yield (blockStart, fileInfo["partSize"] - blockStart, blockByte)

def describe_prg_byte(byte, omitCpuBank, bankSize):
    items = []

    if byte & PRG_CODE:
        if byte & PRG_INDIRECT_CODE:
            items.append("code (indirectly accessed)")
        else:
            items.append("code")

    if byte & PRG_DATA:
        if byte & PRG_INDIRECT_DATA and byte & PRG_PCM_AUDIO:
            items.append("data (indirectly accessed & PCM audio)")
        elif byte & PRG_INDIRECT_DATA:
            items.append("data (indirectly accessed)")
        elif byte & PRG_PCM_AUDIO:
            items.append("data (PCM audio)")
        else:
            items.append("data")

    if byte and not omitCpuBank:
        cpuBankStart = (
            32 + bool(byte & PRG_CPU_BANK_HI) * 16 + bool(byte & PRG_CPU_BANK_LO) * 8
        ) * 1024
        items.append(f"CPU bank 0x{cpuBankStart:04x}-0x{cpuBankStart+bankSize-1:04x}")

    return ", ".join(items) if items else "unaccessed"

def describe_chr_byte(byte):
    items = []
    if byte & CHR_READ_PROGRAMMATICALLY:
        items.append("read programmatically")
    if byte & CHR_RENDERED:
        items.append("rendered")
    return ", ".join(items) if items else "unaccessed"

def generate_cdl_info(handle, args):
    # get info about the CDL file; yield fields of one block per call

    fileInfo = get_file_info(handle.seek(0, 2), args)

    if args.part == "p":
        # CPU bank info is redundant if banks are 32 KiB or there is only one bank
        omitCpuBank = args.bank_size * 1024 in (32 * 1024, fileInfo["partSize"])

    for (romAddr, length, byte) in generate_cdl_blocks(handle, fileInfo, args):
        (bank, offset) = divmod(romAddr, args.bank_size * 1024)
        nesAddr = fileInfo["origin"] + offset
        if args.part == "p":
            descr = describe_prg_byte(byte, omitCpuBank, args.bank_size * 1024)
        else:
            descr = describe_chr_byte(byte)
        if args.output_format == "c":
            yield (romAddr, bank, offset, nesAddr, length, byte, f'"{descr}"')
        else:
            yield (
                f"{romAddr:06x}", f"{bank:02x}", f"{offset:04x}", f"{nesAddr:04x}",
                f"{length:04x}", f"{byte:02x}", descr
            )

def main():
    args = parse_arguments()

    # print CSV/table headers; pick field separator for data
    if args.output_format == "c":
        fieldSeparator = ","
        print(fieldSeparator.join(f'"{f}"' for f in HEADERS))
    else:
        fieldSeparator = " "
        print(", ".join(HEADERS) + " (all numbers in hexadecimal):")

    # print data lines
    try:
        with open(args.input_file, "rb") as handle:
            for fields in generate_cdl_info(handle, args):
                print(fieldSeparator.join(str(f) for f in fields))
    except OSError:
        sys.exit("Error reading the file.")

main()
