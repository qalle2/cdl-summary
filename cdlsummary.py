import getopt
import math
import os.path
import sys

PRG_BANK_SIZE = 16 * 1024
CHR_BANK_SIZE = 8 * 1024

# CDL bitmasks - PRG ROM bytes
PRG_PCM_DATA = 0b0100_0000
PRG_INDIRECT_DATA = 0b0010_0000
PRG_INDIRECT_CODE = 0b0001_0000
PRG_BANK = 0b0000_1100
PRG_DATA = 0b0000_0010
PRG_CODE = 0b0000_0001

# CDL bitmasks - CHR ROM bytes
CHR_READ = 0b0000_0010
CHR_DRAWN = 0b0000_0001

# maximum size of buffer when reading files, in bytes
FILE_BUFFER_MAX_SIZE = 2 ** 20

# for getopt
SHORT_OPTS = "b:p:o:"
LONG_OPTS = (
    "cpu-origin-address=",
    "ignore-cpu-bank",
    "ignore-method",
    "omit-unaccessed",
    "output-format=",
    "part=",
    "prg-rom-banks=",
    "rom-bank-size=",
)

def guess_PRG_size(fileSize):
    """Guess the PRG ROM size based on the CDL file size."""

    # the largest power of two less than the CDL size;
    # that is, half the CDL size, rounded up to the next power of two;
    # exception: at least 16 KiB
    log = math.ceil(math.log2(fileSize))
    return 2 ** max(log - 1, 14)

def parse_ROM_bank_size(ROMBankSize, part):
    """ROMBankSize: str; part: 'P' or 'C'; return an int or exit"""

    try:
        ROMBankSize = int(ROMBankSize, 16)
    except ValueError:
        exit("Error: the bank size must be a hexadecimal integer.")

    if part == "P":
        if ROMBankSize not in (0x1000, 0x2000, 0x4000, 0x8000):
            exit("Error: invalid PRG ROM bank size.")
    else:
        if ROMBankSize not in (0x400, 0x800, 0x1000, 0x2000):
            exit("Error: invalid CHR ROM bank size.")

    return ROMBankSize

def parse_CPU_origin_address(origin, part):
    """origin: None or str; part: 'P' or 'C'; return an int or exit"""

    if origin is None:
        return 0x8000 if part == "P" else 0x0000

    try:
        origin = int(origin, 16)
    except ValueError:
        exit(
            "Error: the CPU/PPU origin address must be a hexadecimal integer."
        )

    if origin < 0x0:
        exit("Error: the CPU/PPU origin address is too small.")
    if origin > 0xfc00 or part == "C" and origin > 0x1c00:
        exit("Error: the CPU/PPU origin address is too large.")
    if origin % 0x400:
        exit(
            "Error: the CPU/PPU origin address is not a multiple of 400 "
            "(hexadecimal)."
        )

    return origin

def parse_arguments():
    """Parse command line arguments using getopt."""

    try:
        (opts, args) = getopt.getopt(sys.argv[1:], SHORT_OPTS, LONG_OPTS)
    except getopt.GetoptError:
        exit("Error: invalid option. See the readme file.")

    if len(args) != 1:
        exit("Error: invalid number of arguments. See the readme file.")

    opts = dict(opts)

    # PRG ROM size
    prgSize = opts.get("--prg-rom-banks", opts.get("-b"))
    if prgSize is not None:
        try:
            prgSize = int(prgSize, 10)
            if not 1 <= prgSize <= 255:
                raise ValueError
        except ValueError:
            exit("Error: invalid number of PRG ROM banks.")
        prgSize *= PRG_BANK_SIZE

    # part
    part = opts.get("--part", opts.get("-p", "P")).upper()
    if part not in ("P", "C"):
        exit("Invalid part argument.")

    # output format
    outputFormat = opts.get("--output-format", opts.get("-o", "L")).upper()
    if outputFormat not in ("L", "S"):
        exit("Invalid output format argument.")

    # switches
    omitUnaccessed = "--omit-unaccessed" in opts
    ignoreMethod = "--ignore-method" in opts
    ignoreCPUBank = "--ignore-cpu-bank" in opts

    # input file
    source = args[0]
    if not os.path.isfile(source):
        exit("Error: file not found.")
    try:
        fileSize = os.path.getsize(source)
    except OSError:
        exit("Error getting input file size.")

    # validate file size (1 PRG bank = 2 CHR banks)
    (CHRBankCount, remainder) = divmod(fileSize, CHR_BANK_SIZE)
    if remainder:
        exit("Error: the file size is not a multiple of 8 KiB.")
    if CHRBankCount < 2:
        exit("Error: the file is too small.")
    if CHRBankCount > 256 * 2 + 255:
        exit("Error: the file is too large.")

    if prgSize is None:
        # guess PRG size
        prgSize = guess_PRG_size(fileSize)
        print("Warning: PRG ROM size not specified, guessing {:d} KiB.".format(
            prgSize // 1024
        ))
    else:
        # validate PRG size
        if prgSize > fileSize:
            exit("Error: the PRG ROM is too large.")
        # validate CHR size
        CHRBankCount = (fileSize - prgSize) // CHR_BANK_SIZE
        if CHRBankCount > 255:
            exit("Error: the PRG ROM is too small.")

    if part == "C" and prgSize == fileSize:
        exit("Error: no CHR ROM to read.")

    # ROM bank size
    ROMBankSize = opts.get("--rom-bank-size")
    if ROMBankSize is None:
        ROMBankSize = min(prgSize, 0x8000) if part == "P" else 0x2000

        if part == "P" and prgSize > 2 * PRG_BANK_SIZE \
        or part == "C" and fileSize - prgSize > CHR_BANK_SIZE:
            print(
                "Warning: ROM bank size not specified, defaulting to "
                "0x{:04x}.".format(ROMBankSize)
            )
    else:
        ROMBankSize = parse_ROM_bank_size(ROMBankSize, part)

    # CPU/PPU origin address
    CPUOriginAddress = opts.get("--cpu-origin-address")
    if CPUOriginAddress is None:
        CPUOriginAddress = 0x10000 - ROMBankSize if part == "P" else 0x0000

        if part == "P" and prgSize > 2 * PRG_BANK_SIZE \
        or part == "C" and fileSize - prgSize > CHR_BANK_SIZE:
            print(
                "Warning: CPU/PPU origin address not specified, defaulting to "
                "0x{:04x}.".format(CPUOriginAddress)
            )
    else:
        CPUOriginAddress = parse_CPU_origin_address(CPUOriginAddress, part)
        if CPUOriginAddress + ROMBankSize \
        > (0x10000 if part == "P" else 0x2000):
            exit(
                "Error: the sum of CPU/PPU origin address and ROM bank size "
                "is too large."
            )

    # get the start position and the length of PRG/CHR ROM
    if part == "P":
        partStart = 0
        partLength = prgSize
    else:
        partStart = prgSize
        partLength = fileSize - prgSize

    return {
        "CPUOriginAddress": CPUOriginAddress,
        "ignoreCPUBank": ignoreCPUBank,
        "ignoreMethod": ignoreMethod,
        "omitUnaccessed": omitUnaccessed,
        "outputFormat": outputFormat,
        "part": part,
        "partLength": partLength,
        "partStart": partStart,
        "ROMBankSize": ROMBankSize,
        "source": source,
    }

def read_file(handle, start, bytesLeft):
    """Yield a slice from a file in chunks."""

    handle.seek(start)
    while bytesLeft > 0:
        chunkSize = min(bytesLeft, FILE_BUFFER_MAX_SIZE)
        yield handle.read(chunkSize)
        bytesLeft -= chunkSize

def validate_CDL_data(handle, settings):
    """Validate bytes in the PRG/CHR ROM part in a CDL file.
    Return None or exit."""

    validationMask = 0b1000_0000 if settings["part"] == "P" else 0b1111_1100
    chunkAddr = settings["partStart"]

    for chunk in read_file(
        handle, settings["partStart"], settings["partLength"]
    ):
        for (pos, byte) in enumerate(chunk):
            if byte & validationMask:
                exit("Error: invalid byte at 0x{:06x}: 0x{:02x}".format(
                    chunkAddr + pos, byte
                ))
        chunkAddr += len(chunk)

    return None

def generate_blocks(handle, settings):
    """Read the PRG ROM or the CHR ROM part from a CDL file.
    Notes:
        - a 'chunk' is a bufferful of unprocessed data
        - a 'block' is a sequence of repeating bytes
    Yield: (address in PRG/CHR ROM, length, value) of one block per call.
    TODO: split to two parts."""

    chunkStart = 0     # start address of current chunk in PRG/CHR ROM
    blockStart = None  # start address of current block in PRG/CHR ROM
    blockByte = None   # current repeating byte value

    # which bits to ignore (clear) in each byte
    if settings["part"] == "P":
        ignoreMask = 0b1111_1111
        if settings["ignoreMethod"]:
            ignoreMask &= 0b1000_1111

        if settings["ignoreCPUBank"] or settings["ROMBankSize"] == 0x8000:
            ignoreMask &= 0b1111_0011
        elif settings["ROMBankSize"] == 0x4000:
            ignoreMask &= 0b1111_1011
    else:
        ignoreMask = 0b1111_1111

    for chunk in read_file(
        handle, settings["partStart"], settings["partLength"]
    ):
        for (pos, byte) in enumerate(chunk):
            byte &= ignoreMask

            if blockByte is None or byte != blockByte \
            or pos % settings["ROMBankSize"] == 0:
                # end current block
                if blockByte is not None:
                    if blockByte != 0x00 or not settings["omitUnaccessed"]:
                        yield (
                            blockStart,
                            chunkStart + pos - blockStart,
                            blockByte
                        )
                # start new block
                blockStart = chunkStart + pos
                blockByte = byte
        # remember distance from the start of PRG/CHR ROM
        chunkStart += len(chunk)

    if blockByte != 0x00 or not settings["omitUnaccessed"]:
        # end last block
        yield (blockStart, settings["partLength"] - blockStart, blockByte)

def format_address(addr, settings):
    """addr: address in the PRG/CHR ROM part of a CDL file
    return: (ROM bank, CPU/PPU address)"""

    (ROMBank, CPUBankOffset) = divmod(addr, settings["ROMBankSize"])
    return (ROMBank, settings["CPUOriginAddress"] + CPUBankOffset)

def format_PRG_byte_description(byte, settings):
    """Describe a PRG CDL byte."""

    if byte == 0x00:
        return "unaccessed"

    items = []

    if byte & PRG_CODE:
        if byte & PRG_INDIRECT_CODE:
            items.append("code (indirectly accessed)")
        else:
            items.append("code")

    if byte & PRG_DATA:
        if byte & PRG_INDIRECT_DATA and byte & PRG_PCM_DATA:
            items.append("data (indirectly accessed & PCM audio)")
        elif byte & PRG_INDIRECT_DATA:
            items.append("data (indirectly accessed)")
        elif byte & PRG_PCM_DATA:
            items.append("data (PCM audio)")
        else:
            items.append("data")

    if settings["ROMBankSize"] < min(0x8000, settings["partLength"]) \
    and not settings["ignoreCPUBank"]:
        CPUBankStart = 0x8000 + ((byte >> 2) & 0b11) * 0x2000
        CPUBankSize = max(settings["ROMBankSize"], 0x2000)
        items.append("last mapped to CPU bank 0x{:04x}-0x{:04x}".format(
            CPUBankStart, CPUBankStart + CPUBankSize - 1
        ))

    return ", ".join(items)

def format_CHR_byte_description(byte):
    """Describe a CHR CDL byte."""

    if byte == 0x00:
        return "unaccessed"

    items = []

    if byte & CHR_READ:
        items.append("read programmatically")
    if byte & CHR_DRAWN:
        items.append("rendered")

    return ", ".join(items)

def long_output(handle, settings):
    """Print output in long (human-readable) format."""

    for (addr, length, byte) in generate_blocks(handle, settings):
        (ROMBank, CPUAddr) = format_address(addr, settings)
        CPUAddrEnd = CPUAddr + length - 1

        if settings["part"] == "P":
            descr = format_PRG_byte_description(byte, settings)
        else:
            descr = format_CHR_byte_description(byte)

        print(
            "ROM bank {:03x}, CPU address {:04x}-{:04x}, length {:04x}: "
            "{:s}".format(ROMBank, CPUAddr, CPUAddrEnd, length, descr)
        )

def short_output(handle, settings):
    """Print output in short (CSV) format."""

    print('"ROM bank","CPU/PPU address","length","CDL byte"')

    for (addr, length, byte) in generate_blocks(handle, settings):
        (ROMBank, CPUAddr) = format_address(addr, settings)

        print(",".join(str(n) for n in (ROMBank, CPUAddr, length, byte)))

def main():
    settings = parse_arguments()

    try:
        with open(settings["source"], "rb") as handle:
            validate_CDL_data(handle, settings)

            if settings["outputFormat"] == "L":
                long_output(handle, settings)
            else:
                short_output(handle, settings)
    except OSError:
        exit("Error reading the file.")

if __name__ == "__main__":
    main()
