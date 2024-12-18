import argparse, os, sys

# a CDL file consists of:
# - data for PRG ROM (1-256 times 16 KiB)
# - data for CHR ROM (0-255 times  8 KiB)

# bitmasks for CDL data bytes;
# see https://fceux.com/web/help/CodeDataLogger.html
PRG_PCM_AUDIO     = 1 << 6
PRG_INDIRECT_DATA = 1 << 5
PRG_INDIRECT_CODE = 1 << 4
PRG_CPU_BANK_HI   = 1 << 3
PRG_CPU_BANK_LO   = 1 << 2
PRG_DATA          = 1 << 1
PRG_CODE          = 1 << 0
CHR_READ_PROGRAMMATICALLY = 1 << 1
CHR_RENDERED              = 1 << 0

TABLE_HEADERS = {
    "p": (  # for PRG ROM
        "PRG ROM address", "Bank", "Offset in bank", "CPU address",
        "CDL byte repeat count", "CDL byte description",
    ),
    "c": (  # for CHR ROM
        "CHR ROM address", "Bank", "Offset in bank", "PPU address",
        "CDL byte repeat count", "CDL byte description",
    ),
}

# --- argument parsing --------------------------------------------------------

def parse_args():
    # parse command line arguments using argparse

    parser = argparse.ArgumentParser(
        description="Print an FCEUX Code/Data Logger file (.cdl) in human-"
        "readable format. See README.md for details."
    )

    parser.add_argument("-r", "--prg-size", type=int, required=True)
    parser.add_argument("-p", "--part", choices=("p", "c"), default="p")
    parser.add_argument(
        "-b", "--bank-size", type=int, choices=(1, 2, 4, 8, 16, 32)
    )
    parser.add_argument(
        "-o", "--origin", type=int,
        choices=(0, 1, 2, 3, 4, 5, 6, 7, 32, 40, 48, 56)
    )
    parser.add_argument("--ignore-access-method", action="store_true")
    parser.add_argument(
        "-f", "--output-format", choices=("c", "t"), default="c"
    )
    parser.add_argument("input_file")

    args = parser.parse_args()

    # validate PRG size, bank size and origin
    if args.prg_size % 16 or not 16 <= args.prg_size <= 256 * 16:
        sys.exit("PRG ROM size must be 16-4096 and a multiple of 16.")
    if args.bank_size is not None:
        if args.part == "p" and args.bank_size < 8:
            sys.exit("PRG ROM bank size must be 8/16/32.")
        if args.part == "c" and args.bank_size > 8:
            sys.exit("CHR ROM bank size must be 1/2/4/8.")
        if args.part == "p" and args.prg_size % args.bank_size > 0:
            sys.exit("PRG ROM size must be a multiple of PRG ROM bank size.")
    if args.origin is not None:
        if args.part == "p":
            if args.origin < 32:
                sys.exit("CPU origin address must be 32/40/48/56.")
            if args.origin > 64 - args.bank_size:
                sys.exit(
                    "CPU origin address must be 64 minus PRG bank size or "
                    "less."
                )
        else:
            if args.origin > 7:
                sys.exit("PPU origin address must be 0-7.")
            if args.origin > 8 - args.bank_size:
                sys.exit(
                    "PPU origin address must be 8 minus CHR bank size or less."
                )

    # validate file size against the numbers we just validated
    if not os.path.isfile(args.input_file):
        sys.exit("Input file not found.")
    try:
        fileSize = os.path.getsize(args.input_file)
    except OSError:
        sys.exit("Error getting input file size.")
    if (
        fileSize % (8 * 1024)
        or not 16 * 1024 <= fileSize <= (256 * 16 + 255 * 8) * 1024
    ):
        sys.exit(
            "Input file size must be 16-6136 KiB and a multiple of 8 KiB."
        )
    if fileSize > (args.prg_size + 255 * 8) * 1024:
        sys.exit(
            "Specified PRG ROM size is too small for input file size (CHR ROM "
            "would be too large)."
        )
    if args.part == "c" and fileSize == args.prg_size * 1024:
        sys.exit("Input file has no CHR ROM.")

    return args

# --- input file parsing ------------------------------------------------------

def generate_cdl_blocks(handle, addrRange, bitmask, bankSize):
    # read PRG/CHR ROM from CDL file
    # generate: (rom_address, length, value) for each block (sequence of
    #           repeating bytes)

    blockStart = None  # start address of current block
    blockByte  = None  # current repeating byte value

    handle.seek(addrRange.start)

    for (pos, byte) in enumerate(handle.read(len(addrRange))):
        byte &= bitmask
        if blockByte is None:
            # start a new block
            blockStart = pos
            blockByte  = byte
        elif byte != blockByte or pos % bankSize == 0:
            # end the current block, start a new one
            yield (blockStart, pos - blockStart, blockByte)
            blockStart = pos
            blockByte  = byte

    # end the last block
    yield (blockStart, len(addrRange) - blockStart, blockByte)

def describe_prg_byte(byte, omitCpuBank, bankSize):
    # return a string

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

    if byte & (PRG_CODE | PRG_DATA) and not omitCpuBank:
        cpuBankStart = (
            32
            + bool(byte & PRG_CPU_BANK_HI) * 16
            + bool(byte & PRG_CPU_BANK_LO) *  8
        ) * 1024
        items.append(
            f"CPU bank 0x{cpuBankStart:04x}-0x{cpuBankStart+bankSize-1:04x}"
        )

    return ", ".join(items) if items else "unaccessed"

def describe_chr_byte(byte):
    # return a string

    items = []
    if byte & CHR_READ_PROGRAMMATICALLY:
        items.append("read programmatically")
    if byte & CHR_RENDERED:
        items.append("rendered")
    return ", ".join(items) if items else "unaccessed"

def get_cdl_info(handle, args):
    # get info about the CDL file; generate fields of one block per call

    # addresses to read from CDL file
    if args.part == "p":
        addrRange = range(0, args.prg_size * 1024)
    else:
        addrRange = range(args.prg_size * 1024, handle.seek(0, os.SEEK_END))

    # bank size
    if args.bank_size is not None:
        bankSize = args.bank_size * 1024
    elif args.part == "p":
        bankSize = min(args.prg_size, 32) * 1024
    else:
        bankSize = 8 * 1024

    # start address of each bank
    if args.origin is not None:
        origin = args.origin * 1024
    elif args.part == "p":
        origin = 64 * 1024 - bankSize
    else:
        origin = 0

    # bitmask to AND each CDL byte with
    if args.part == "p":
        bitmask = PRG_DATA | PRG_CODE
        if not args.ignore_access_method:
            bitmask |= PRG_PCM_AUDIO | PRG_INDIRECT_DATA | PRG_INDIRECT_CODE
        if bankSize <= 16 * 1024:
            bitmask |= PRG_CPU_BANK_HI
            if bankSize == 8 * 1024:
                bitmask |= PRG_CPU_BANK_LO
    else:
        bitmask = CHR_READ_PROGRAMMATICALLY | CHR_RENDERED

    # CPU bank info is redundant if banks are 32 KiB or there's only 1 bank
    if args.part == "p":
        omitCpuBank = (bankSize in (32 * 1024, args.prg_size * 1024))
    else:
        omitCpuBank = False  # N/A

    for (romAddr, length, byte) in generate_cdl_blocks(
        handle, addrRange, bitmask, bankSize
    ):
        (bank, offset) = divmod(romAddr, bankSize)
        nesAddr = origin + offset
        if args.part == "p":
            descr = describe_prg_byte(byte, omitCpuBank, bankSize)
        else:
            descr = describe_chr_byte(byte)
        yield (romAddr, bank, offset, nesAddr, length, descr)

# -----------------------------------------------------------------------------

def format_csv_line(fields):
    return ",".join(
        (f'"{f}"' if isinstance(f, str) else str(f)) for f in fields
    )

def main():
    args = parse_args()

    # print CSV/table header
    if args.output_format == "c":
        print(format_csv_line(TABLE_HEADERS[args.part]))
    else:
        print(", ".join(TABLE_HEADERS[args.part]) + ":")
        print()

    # print data lines
    try:
        with open(args.input_file, "rb") as handle:
            for fields in get_cdl_info(handle, args):
                if args.output_format == "c":
                    print(format_csv_line(fields))
                else:
                    print("  ".join(
                        format(f, c) for (f, c)
                        in zip(fields, ("6x", "2x", "4x", "4x", "4x", ""))
                    ))
    except OSError:
        sys.exit("Error reading input file.")

main()
