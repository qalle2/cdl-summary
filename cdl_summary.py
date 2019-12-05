"""Prints a summary of an FCEUX Code/Data Logger file (.cdl)."""

import getopt
import math
import os
import sys

def parse_integer(value, min_, max_, description):
    """Parse integer from command line arguments."""

    try:
        value = int(value, 0)
        if min_ is not None and value < min_:
            raise ValueError
        if max_ is not None and value > max_:
            raise ValueError
    except ValueError:
        sys.exit("Invalid command line integer argument: " + description)
    return value

def get_source_size(source):
    """Get source file size."""

    if not os.path.isfile(source):
        sys.exit("Input file not found.")
    try:
        fileSize = os.path.getsize(source)
    except OSError:
        sys.exit("Error getting input file size.")
    # get size in CHR banks (1 PRG bank = 2 CHR banks)
    (CHRBankCount, remainder) = divmod(fileSize, 0x2000)
    # must be (1 PRG bank + 0 CHR banks) to (256 PRG banks + 255 CHR banks)
    if remainder or not 2 <= CHRBankCount <= 256 * 2 + 255:
        sys.exit("Invalid input file size.")
    return fileSize

def get_PRG_ROM_bank_count(bankCnt, fileSize):
    """Parse and validate PRG ROM bank count (string/None) from command line arguments."""

    # get minimum and maximum bank counts (too small a PRG ROM would result in too large a CHR ROM)
    min_ = max(1, math.ceil((fileSize - 255 * 0x2000) / 0x4000))
    max_ = min(256, fileSize // 0x4000)
    if bankCnt is not None:
        # validate
        return parse_integer(bankCnt, min_, max_, "number of PRG ROM banks")
    # guess
    if fileSize in (0x4000, 256 * 0x4000):
        # exceptions to the formula below
        bankCnt = fileSize // 0x4000
    else:
        # the largest power of two that's smaller than the file size
        bankCnt = 2 ** (math.ceil(math.log2(fileSize / 0x4000)) - 1)
    assert min_ <= bankCnt <= max_
    print("Guessing PRG ROM bank count: {:d}".format(bankCnt))
    return bankCnt

def get_ROM_bank_size(bankSize, part, PRGBankCnt):
    """Parse and validate ROM bank size (string/None) from command line arguments."""

    if bankSize is not None:
        return parse_integer(bankSize, 0x100, 0x8000 if part == "P" else 0x2000, "ROM bank size")
    # guess
    bankSize = min(PRGBankCnt * 0x4000, 0x8000) if part == "P" else 0x2000
    print("Guessing ROM bank size: 0x{:04x}".format(bankSize))
    return bankSize

def get_origin(origin, part, bankSize):
    """Parse and validate CPU/PPU origin address (string/None) from command line arguments."""

    if origin is not None:
        # validate
        min_ = 0x8000 if part == "P" else 0
        max_ = 0x10000 - bankSize if part == "P" else 0x2000 - bankSize
        return parse_integer(origin, min_, max_, "CPU/PPU origin address")
    # guess
    origin = 0x10000 - bankSize if part == "P" else 0
    print("Guessing {:s} origin address: 0x{:04x}".format(
        "CPU" if part == "P" else "PPU", origin
    ))
    return origin

def parse_arguments():
    """Parse command line arguments using getopt."""

    shortOpts = "b:p:umr:o:c"
    longOpts = (
        "cpu-origin-address=",
        "csv",
        "ignore-cpu-bank",
        "ignore-directness",
        "ignore-method",
        "ignore-pcm",
        "omit-unaccessed",
        "part=",
        "prg-rom-banks=",
        "rom-bank-size=",
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
    fileSize = get_source_size(source)

    # PRG ROM size
    PRGBankCnt = get_PRG_ROM_bank_count(opts.get("--prg-rom-banks", opts.get("-b")), fileSize)
    PRGSize = PRGBankCnt * 0x4000
    if part == "C" and PRGSize == fileSize:
        sys.exit("No CHR ROM.")

    # ROM bank size
    bankSize = get_ROM_bank_size(opts.get("--rom-bank-size", opts.get("-r")), part, PRGBankCnt)

    # CPU/PPU origin address
    origin = get_origin(opts.get("--origin", opts.get("-o")), part, bankSize)

    return {
        "origin": origin,
        "CSVOutput": "-c" in opts or "--csv" in opts,
        "ignoreCPUBank": "--ignore-cpu-bank" in opts,
        "ignoreDirectness": "--ignore-directness" in opts,
        "ignoreMethod": "-m" in opts or "--ignore-method" in opts,
        "ignorePCM": "--ignore-pcm" in opts,
        "omitUnaccessed": "-u" in opts or "--omit-unaccessed" in opts,
        "part": part,
        "partSize": PRGSize if part == "P" else fileSize - PRGSize,
        "partStart": 0 if part == "P" else PRGSize,
        "bankSize": bankSize,
        "source": source,
    }

def read_file(handle, start, bytesLeft):
    """Read a part of a file. Yield one chunk per call."""

    handle.seek(start)
    while bytesLeft > 0:
        chunkSize = min(bytesLeft, 2 ** 20)
        yield handle.read(chunkSize)
        bytesLeft -= chunkSize

def validate_CDL_data(handle, settings):
    """Validate bytes in the PRG/CHR ROM part in a CDL file. Exit on error."""

    validationMask = 0b1000_0000 if settings["part"] == "P" else 0b1111_1100
    chunkAddr = settings["partStart"]

    for chunk in read_file(handle, settings["partStart"], settings["partSize"]):
        for (pos, byte) in enumerate(chunk):
            if byte & validationMask:
                sys.exit("Error: invalid byte at 0x{:06x}: 0x{:02x}".format(
                    chunkAddr + pos, byte
                ))
        chunkAddr += len(chunk)

def generate_blocks(handle, settings):
    """Read the PRG ROM or the CHR ROM part from a CDL file.
    Notes:
        - a 'chunk' is a bufferful of unprocessed data
        - a 'block' is a sequence of repeating bytes
    Yield: (address in PRG/CHR ROM, length, value) of one block per call."""

    chunkStart = 0     # start address of current chunk in PRG/CHR ROM
    blockStart = None  # start address of current block in PRG/CHR ROM
    blockByte = None   # current repeating byte value

    # which bits to ignore (clear) in each PRG data byte
    if settings["part"] == "P":
        # PRG ROM
        ignoreMask = 0b0111_1111  # unused bits
        if settings["ignorePCM"]:
            ignoreMask &= 0b1011_1111
        if settings["ignoreDirectness"]:
            ignoreMask &= 0b1100_1111
        if settings["ignoreCPUBank"] or settings["bankSize"] == 0x8000:
            ignoreMask &= 0b1111_0011
        elif settings["bankSize"] == 0x4000:
            ignoreMask &= 0b1111_1011
    else:
        # CHR ROM
        ignoreMask = 0b0000_0011  # unused bits

    for chunk in read_file(handle, settings["partStart"], settings["partSize"]):
        for (pos, byte) in enumerate(chunk):
            byte &= ignoreMask
            if settings["ignoreMethod"]:
                byte = int(bool(byte))  # any nonzero value -> 1

            if blockByte is None or byte != blockByte or pos % settings["bankSize"] == 0:
                # end current block
                if blockByte is not None:
                    if blockByte or not settings["omitUnaccessed"]:
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

    if blockByte or not settings["omitUnaccessed"]:
        # end last block
        yield (blockStart, settings["partSize"] - blockStart, blockByte)

def format_address(addr, settings):
    """addr: address in the PRG/CHR ROM part of a CDL file
    return: (ROM bank, CPU/PPU address)"""

    (ROMBank, CPUBankOffset) = divmod(addr, settings["bankSize"])
    return (ROMBank, settings["origin"] + CPUBankOffset)

def PRG_byte_description(byte, settings):
    """Describe a PRG CDL byte."""

    if settings["ignoreMethod"] and byte:
        return "accessed"

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

    if items and settings["bankSize"] < settings["partSize"] and not settings["ignoreCPUBank"]:
        CPUBankStart = 0x8000 + ((byte >> 2) & 0b11) * 0x2000
        CPUBankSize = max(settings["bankSize"], 0x2000)
        items.append("last mapped to CPU bank 0x{:04x}-0x{:04x}".format(
            CPUBankStart, CPUBankStart + CPUBankSize - 1
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

    for (addr, length, byte) in generate_blocks(handle, settings):
        (ROMBank, CPUAddr) = format_address(addr, settings)
        CPUAddrEnd = CPUAddr + length - 1
        if settings["part"] == "P":
            descr = PRG_byte_description(byte, settings)
        else:
            descr = CHR_byte_description(byte, settings)
        print("ROM bank {:03x}, {:s} address {:04x}-{:04x} (length {:4x}): {:s}".format(
            ROMBank, "CPU" if settings["part"] == "P" else "PPU", CPUAddr, CPUAddrEnd, length, descr
        ))

def CSV_output(handle, settings):
    """Print output in CSV (machine-readable) format."""

    print('"ROM bank","CPU/PPU address","length","CDL byte"')
    for (addr, length, byte) in generate_blocks(handle, settings):
        (ROMBank, CPUAddr) = format_address(addr, settings)
        print(",".join(str(n) for n in (ROMBank, CPUAddr, length, byte)))

def main():
    """The main function."""

    settings = parse_arguments()
    try:
        with open(settings["source"], "rb") as handle:
            validate_CDL_data(handle, settings)
            if settings["CSVOutput"]:
                CSV_output(handle, settings)
            else:
                normal_output(handle, settings)
    except OSError:
        sys.exit("Error reading the file.")

if __name__ == "__main__":
    main()
