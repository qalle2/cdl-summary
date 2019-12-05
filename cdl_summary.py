"""Prints a summary of an FCEUX Code/Data Logger file (.cdl)."""

import getopt
import math
import os
import sys

def parse_integer(value, min_, max_, description):
    """Parse a string from command line arguments as an integer and validate it.
    value: string to parse&validate
    min_: minimum value or None
    max_: maximum value or None
    description: for the error message
    return: parsed value"""

    try:
        value = int(value, 0)
        if min_ is not None and value < min_:
            raise ValueError
        if max_ is not None and value > max_:
            raise ValueError
    except ValueError:
        sys.exit("Invalid command line integer argument: " + description)
    return value

def get_source_size(handle):
    """Get the size of the CDL file.
    handle: file handle
    return: file size in 8-KiB units"""

    if not os.path.isfile(handle):
        sys.exit("Input file not found.")
    try:
        fileSize = os.path.getsize(handle)
    except OSError:
        sys.exit("Error getting input file size.")
    # get size in 8-KiB units
    (fileSize8KiB, remainder) = divmod(fileSize, 0x2000)
    # the size must be a multiple of 8 KiB
    # and from 16 KiB (16 KiB PRG + 0 KiB CHR) to 6136 KiB (4096 KiB PRG + 2040 KiB CHR)
    if remainder or not 2 <= fileSize8KiB <= 767:
        sys.exit("Invalid input file size.")
    return fileSize8KiB

def guess_PRG_ROM_size(fileSize8KiB):
    """Guess the size of the PRG ROM part of the CDL file.
    fileSize8KiB: CDL file size in 8-KiB units (2-767)
    return: PRG ROM size in 16-KiB units (1-256)"""

    if fileSize8KiB in (2, 512):
        return fileSize8KiB // 2
    # the largest power of two that's smaller than the file size
    return 2 ** (math.ceil(math.log2(fileSize8KiB)) - 2)

def get_PRG_ROM_size(PRGSize16KiB, fileSize8KiB):
    """Get the size of the PRG ROM part of the CDL file from the command line argument or guess it.
    PRGSize16KiB: PRG ROM size in 16-KiB units (string) or None (will be guessed)
    fileSize8KiB: CDL file size in 8-KiB units
    return: PRG ROM size in 16-KiB units"""

    # get minimum and maximum PRG ROM size from file size (in 16-KiB units; too small a PRG ROM
    # would result in a CHR ROM larger than 255 * 8 KiB)
    PRGSize16KiBMin = max(1, (fileSize8KiB - 254) // 2)
    PRGSize16KiBMax = min(256, fileSize8KiB // 2)
    assert 0 <= fileSize8KiB - PRGSize16KiBMax * 2 <= fileSize8KiB - PRGSize16KiBMin * 2 <= 255
    if PRGSize16KiB is not None:
        # parse&validate
        return parse_integer(PRGSize16KiB, PRGSize16KiBMin, PRGSize16KiBMax, "PRG ROM size")
    # guess
    PRGSize16KiB = guess_PRG_ROM_size(fileSize8KiB)
    assert PRGSize16KiBMin <= PRGSize16KiB <= PRGSize16KiBMax
    print(f"Guessing PRG ROM size: {PRGSize16KiB:d} * 16 KiB")
    return PRGSize16KiB

def get_ROM_bank_size(bankSize, part, PRGSize16KiB):
    """Get the size of ROM banks the from command line argument or guess it.
    bankSize: ROM bank size (string) or None (will be guessed)
    part: part of the CDL file to read
    PRGSize16KiB: PRG ROM size in 16-KiB units"""

    if part == "P":
        # 32 KiB if a multiple of it, otherwise 16 KiB
        maxBankSize = 0x4000 if PRGSize16KiB % 2 else 0x8000
    else:
        maxBankSize = 0x2000  # 8 KiB
    if bankSize is not None:
        # parse&validate
        bankSize = parse_integer(bankSize, 0x1000, maxBankSize, "ROM bank size")
        if bankSize not in (0x1000, 0x2000, 0x4000, 0x8000):
            sys.exit("ROM bank size must be a power of two.")
    else:
        # guess
        bankSize = maxBankSize
        print(f"Guessing ROM bank size: 0x{bankSize:04x}")
    return bankSize

def get_origin(origin, part, bankSize):
    """Parse and validate CPU/PPU origin address (string/None) from command line arguments."""

    if origin is not None:
        # parse&validate
        min_ = 0x8000 if part == "P" else 0
        max_ = 0x10000 - bankSize if part == "P" else 0x2000 - bankSize
        origin = parse_integer(origin, min_, max_, "CPU/PPU origin address")
        if origin % 0x1000:
            sys.exit("Origin must be a multiple of 0x1000.")
        return origin
    # guess
    origin = 0x10000 - bankSize if part == "P" else 0
    print("Guessing {:s} origin address: 0x{:04x}".format("CPU" if part == "P" else "PPU", origin))
    return origin

def parse_arguments():
    """Parse command line arguments using getopt."""

    shortOpts = "g:p:r:o:muc"
    longOpts = (
        # switches
        "ignore-method",
        "ignore-directness",
        "ignore-pcm",
        "ignore-cpu-bank",
        "omit-unaccessed",
        "csv",
        # other options
        "prg-rom-size=",
        "part=",
        "rom-bank-size=",
        "origin=",
    )
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], shortOpts, longOpts)
    except getopt.GetoptError:
        sys.exit("Invalid command line argument.")
    opts = dict(opts)

    # the part to read (PRG/CHR ROM)
    part = opts.get("--part", opts.get("-p", "P")).upper()
    if part not in ("P", "C"):
        sys.exit("Invalid command line argument: which part to read")

    # source file
    if len(args) != 1:
        sys.exit("Invalid number of command line arguments.")
    source = args[0]
    fileSize8KiB = get_source_size(source)

    # PRG ROM size
    PRGSize16KiB = get_PRG_ROM_size(opts.get("--prg-rom-size", opts.get("-g")), fileSize8KiB)
    PRGSize = PRGSize16KiB * 0x4000
    if part == "C" and fileSize8KiB == PRGSize16KiB * 2:
        sys.exit("No CHR ROM.")

    # ROM bank size
    bankSize = get_ROM_bank_size(opts.get("--rom-bank-size", opts.get("-r")), part, PRGSize16KiB)

    # CPU/PPU origin address
    origin = get_origin(opts.get("--origin", opts.get("-o")), part, bankSize)

    return {
        # switches
        "ignoreMethod": "-m" in opts or "--ignore-method" in opts,
        "ignoreDirectness": "--ignore-directness" in opts,
        "ignorePCM": "--ignore-pcm" in opts,
        "ignoreCPUBank": "--ignore-cpu-bank" in opts,
        "omitUnaccessed": "-u" in opts or "--omit-unaccessed" in opts,
        "CSVOutput": "-c" in opts or "--csv" in opts,
        # other options
        "part": part,
        "partSize": PRGSize if part == "P" else fileSize8KiB * 0x2000 - PRGSize,
        "partStart": 0 if part == "P" else PRGSize,
        "bankSize": bankSize,
        "origin": origin,
        # required argument
        "source": source,
    }

def read_file(handle, start, bytesLeft):
    """Read a part of a file. Yield one chunk per call."""

    handle.seek(start)
    while bytesLeft > 0:
        chunkSize = min(bytesLeft, 2 ** 20)
        yield handle.read(chunkSize)
        bytesLeft -= chunkSize

def get_ignore_mask(settings):
    """Create an AND bitmask for clearing unwanted bits in each CDL byte."""

    if settings["part"] == "P":
        # PRG ROM
        mask = 0b0111_1111  # unused bits
        if settings["ignorePCM"]:
            mask &= 0b1011_1111
        if settings["ignoreDirectness"]:
            mask &= 0b1100_1111
        if settings["ignoreCPUBank"] or settings["bankSize"] == 0x8000:
            mask &= 0b1111_0011
        elif settings["bankSize"] == 0x4000:
            mask &= 0b1111_1011
        return mask
    # CHR ROM
    return 0b0000_0011  # unused bits

def generate_blocks(handle, settings):
    """Read the PRG ROM or the CHR ROM part from a CDL file.
    Notes:
        - a 'chunk' is a bufferful of unprocessed data
        - a 'block' is a sequence of repeating bytes
    Yield: (address in PRG/CHR ROM, length, value) of one block per call."""

    chunkStart = 0     # start address of current chunk in PRG/CHR ROM
    blockStart = None  # start address of current block in PRG/CHR ROM
    blockByte = None   # current repeating byte value

    ignoreMask = get_ignore_mask(settings)

    for chunk in read_file(handle, settings["partStart"], settings["partSize"]):
        for (pos, byte) in enumerate(chunk):
            byte &= ignoreMask
            if settings["ignoreMethod"]:
                byte = int(bool(byte))  # any nonzero value -> 1
            if blockByte is None or byte != blockByte or pos % settings["bankSize"] == 0:
                if blockByte is not None:
                    # end current block
                    if blockByte or not settings["omitUnaccessed"]:
                        yield (blockStart, chunkStart + pos - blockStart, blockByte)
                # start new block
                blockStart = chunkStart + pos
                blockByte = byte
        # remember distance from the start of PRG/CHR ROM
        chunkStart += len(chunk)

    if blockByte or not settings["omitUnaccessed"]:
        # end last block
        yield (blockStart, settings["partSize"] - blockStart, blockByte)

def convert_address(addr, settings):
    """addr: address in the PRG/CHR ROM part of a CDL file
    return: (bank, offset, NES address)"""

    (bank, offset) = divmod(addr, settings["bankSize"])
    return (bank, offset, settings["origin"] + offset)

def PRG_byte_description(byte, settings):
    """Describe a PRG CDL byte."""

    if settings["ignoreMethod"]:
        return "accessed" if byte else "unaccessed"

    items = []
    if byte & 0b0000_0001:
        # code
        if byte & 0b0001_0000:
            items.append("code (indirectly accessed)")
        else:
            items.append("code")
    if byte & 0b0000_0010:
        # data
        if byte & 0b0110_0000 == 0b0110_0000:
            items.append("data (indirectly accessed & PCM audio)")
        elif byte & 0b0010_0000:
            items.append("data (indirectly accessed)")
        elif byte & 0b0100_0000:
            items.append("data (PCM audio)")
        else:
            items.append("data")
    # CPU bank (only for accessed bytes)
    if byte and settings["bankSize"] < 0x8000 and not settings["ignoreCPUBank"]:
        bankStart = 0x8000 + ((byte & 0b0000_1100) >> 2) * 0x2000
        bankSize = max(settings["bankSize"], 0x2000)
        items.append("last mapped to CPU bank 0x{:04x}-0x{:04x}".format(
            bankStart, bankStart + bankSize - 1
        ))
    return ", ".join(items) if items else "unaccessed"

def CHR_byte_description(byte, settings):
    """Describe a CHR CDL byte."""

    if settings["ignoreMethod"] and byte:
        return "accessed"
    if byte & 0b0000_0011 == 0b0000_0011:
        return "read programmatically & rendered"
    if byte & 0b0000_0010:
        return "read programmatically"
    if byte & 0b0000_0001:
        return "rendered"
    return "unaccessed"

def normal_output(handle, settings):
    """Print output in human-readable format."""

    byteDescriptionFn = PRG_byte_description if settings["part"] == "P" else CHR_byte_description
    partDescr = "PRG" if settings["part"] == "P" else "CHR"
    chip = "CPU" if settings["part"] == "P" else "PPU"
    for (addr, length, byte) in generate_blocks(handle, settings):
        (bank, offset, NESAddr) = convert_address(addr, settings)
        descr = byteDescriptionFn(byte, settings)
        print(
            "{:s} {:06x}-{:06x}, bank {:03x}, off {:04x}-{:04x}, {:s} {:04x}-{:04x}, len {:04x}: "
            "{:s}".format(
                partDescr, addr, addr + length - 1,  # PRG/CHR ROM address range
                bank, offset, offset + length - 1,  # ROM bank and address range within it
                chip, NESAddr, NESAddr + length - 1,  # CPU/PPU address range
                length, descr
            )
        )

def CSV_output(handle, settings):
    """Print output in CSV (machine-readable) format."""

    byteDescriptionFn = PRG_byte_description if settings["part"] == "P" else CHR_byte_description
    for (addr, length, byte) in generate_blocks(handle, settings):
        (bank, offset, NESAddr) = convert_address(addr, settings)
        descr = byteDescriptionFn(byte, settings)
        print(",".join(str(n) for n in (addr, bank, offset, NESAddr, length, byte, f'"{descr:s}"')))

def main():
    """The main function."""

    settings = parse_arguments()
    try:
        with open(settings["source"], "rb") as handle:
            if settings["CSVOutput"]:
                CSV_output(handle, settings)
            else:
                normal_output(handle, settings)
    except OSError:
        sys.exit("Error reading the file.")

if __name__ == "__main__":
    main()
