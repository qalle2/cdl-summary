"""Prints a summary of an FCEUX Code/Data Logger file (.cdl).
TODO: test"""

import argparse
import math
import os
import sys

def parse_arguments():
    """Parse command line arguments using argparse.
    TODO: pylint complains"""

    parser = argparse.ArgumentParser(
        description="Print an FCEUX Code/Data Logger file (.cdl) in human-readable format."
    )

    parser.add_argument(
        "-g", "--prg_rom_size", type=int,
        help="The PRG ROM size of the input file, in KiB (16-4096 and a multiple of 16, usually a "
        "power of two). Omit to guess."
    )
    parser.add_argument(
        "-p", "--part", choices=("p", "c"), default="p",
        help="Which part to read from the input file. p=PRG ROM (default), c=CHR ROM. -d/-a/-b "
        "can't be used with CHR ROM."
    )
    parser.add_argument(
        "-o", "--origin", type=int, choices=(0, 1, 2, 3, 4, 5, 6, 7, 32, 40, 48, 56),
        help="The CPU/PPU address each ROM bank starts from, in KiB. 32/40/48/56 for PRG ROM "
        "(default=32), 0-7 for CHR ROM (default=0)."
    )
    parser.add_argument(
        "-r", "--bank-size", choices=(0, 1, 2, 4, 8, 16, 32),
        help="Size of PRG/CHR ROM banks in KiB. 8/16/32 for PRG ROM (default=32), 1/2/4/8 for CHR "
        "ROM (default=8). -o plus -r must be 64 or less for PRG ROM and 8 or less for CHR ROM."
    )
    parser.add_argument(
        "-m", "--ignore-method", action="store_true",
        help="Ignore how bytes were accessed. Overrides -d/-a/-b."
    )
    parser.add_argument(
        "-d", "--ignore-directness", action="store_true",
        help="Ignore whether PRG ROM bytes were accessed directly or indirectly."
    )
    parser.add_argument(
        "-a", "--ignore-pcm", action="store_true",
        help="Ignore whether PRG ROM bytes were accessed as PCM audio data."
    )
    parser.add_argument(
        "-b", "--ignore-bank", action="store_true",
        help="Ignore which CPU bank PRG ROM bytes were mapped to when last accessed."
    )
    parser.add_argument(
        "input_file", help="The .cdl file to read. Size: 16-6136 KiB and a multiple of 8 KiB."
    )

    args = parser.parse_args()

    # validate input file
    if not os.path.isfile(args.input_file):
        sys.exit("Input file not found.")

    # validate PRG ROM size
    if args.prg_rom_size is not None:
        (PRGSize16KiB, remainder) = divmod(args.prg_rom_size, 16)
        if not 1 <= PRGSize16KiB <= 256 or remainder:
            sys.exit("Invalid PRG ROM size.")

    # validate origin and ROM bank size (their sum is validated later)
    if args.part == "p":
        if args.origin is not None:
            if args.origin < 32:
                sys.exit("Invalid CPU origin address.")
        if args.bank_size is not None:
            if args.bank_size < 8:
                sys.exit("Invalid PRG ROM bank size.")
    else:
        if args.origin is not None:
            if args.origin > 7:
                sys.exit("Invalid PPU origin address.")
        if args.bank_size is not None:
            if args.bank_size > 8:
                sys.exit("Invalid CHR ROM bank size.")

    # validate switches
    if args.part == "c" and (args.ignore_directness or args.ignore_pcm or args.ignore_bank):
        sys.exit("-d/-a/-b can't be used with CHR ROM.")

    return args

# --------------------------------------------------------------------------------------------------

def get_CDL_size(handle):
    """Get the size of the CDL file."""

    fileSize = handle.seek(0, 2)
    (fileSize8KiB, remainder) = divmod(fileSize, 8 * 1024)
    # minimum: 16 KiB PRG + 0 KiB CHR; maximum: 256 * 16 KiB PRG + 255 * 8 KiB CHR
    if not 2 <= fileSize8KiB <= 256 * 2 + 255 or remainder:
        sys.exit("Invalid input file size.")
    return fileSize8KiB * 8 * 1024

def get_PRG_ROM_size(PRGSizeKiB, fileSize):
    """Validate the PRG ROM size or guess it (if None). Return the size."""

    # get size in bytes or guess it
    if PRGSizeKiB is not None:
        PRGSize = PRGSizeKiB * 1024
    elif fileSize in (16 * 1024, 256 * 16 * 1024):
        # must be all PRG ROM (a 256 * 16 KiB file can't be half CHR ROM)
        PRGSize = fileSize
    else:
        # the largest power of two that's smaller than the file size
        PRGSize = 2 ** (math.ceil(math.log2(fileSize)) - 1)
    # validate the size
    if PRGSize > fileSize or fileSize - PRGSize > 255 * 8 * 1024:
        # can't have more than 255 * 8 KiB CHR ROM
        sys.exit("Invalid PRG ROM size specified.")
    return PRGSize

def get_PRG_ROM_bank_size(bankSizeKiB, PRGSize):
    """Get PRG ROM bank size."""

    if bankSizeKiB is not None:
        bankSize = bankSizeKiB * 1024
        if PRGSize % bankSize:
            sys.exit("Total PRG ROM size must be a multiple of PRG ROM bank size.")
    else:
        bankSize = 16 * 1024 if PRGSize % (32 * 1024) else 32 * 1024
        print("Warning: guessing PRG bank size: {:d} bytes".format(bankSize), file=sys.stderr)
    return bankSize

def get_CHR_ROM_bank_size(bankSizeKiB):
    """Get CHR ROM bank size."""

    if bankSizeKiB is not None:
        bankSize = bankSizeKiB * 1024  # always valid
    else:
        bankSize = 8 * 1024  # always valid
        print("Warning: guessing CHR bank size: {:d} bytes".format(bankSize), file=sys.stderr)
    return bankSize

def get_origin(originKiB, max_):
    """Get CPU/PPU address origin."""

    if originKiB is not None:
        origin = originKiB * 1024
        if origin > max_:
            sys.exit("The sum of CPU/PPU address origin and PRG/CHR ROM bank size is too large.")
    else:
        origin = max_
    return origin

def get_PRG_ignore_mask(args, bankSize):
    """Create an AND bitmask for clearing unwanted bits in each PRG CDL byte."""

    mask = 0b0111_1111
    if args.ignore_pcm:
        mask &= 0b1011_1111
    if args.ignore_directness:
        mask &= 0b1100_1111
    if args.ignore_bank or bankSize == 32 * 1024:
        mask &= 0b1111_0011
    elif bankSize == 16 * 1024:
        mask &= 0b1111_1011
    return mask

def get_file_info(handle, args):
    """Get more info on what to do based on args and file size."""

    fileSize = get_CDL_size(handle)
    PRGSize = get_PRG_ROM_size(args.prg_rom_size, fileSize)

    fileInfo = {}
    fileInfo["partStart"] = 0 if args.part == "p" else PRGSize
    fileInfo["partSize"] = PRGSize if args.part == "p" else fileSize - PRGSize
    if fileInfo["partSize"] == 0:
        sys.exit("No CHR ROM (the file is all PRG ROM).")

    if args.part == "p":
        fileInfo["bankSize"] = get_PRG_ROM_bank_size(args.bank_size, PRGSize)
        fileInfo["origin"] = get_origin(args.origin, 64 * 1024 - fileInfo["bankSize"])
        fileInfo["ignoreMask"] = get_PRG_ignore_mask(args, fileInfo["bankSize"])
    else:
        fileInfo["bankSize"] = get_CHR_ROM_bank_size(args.bank_size)
        fileInfo["origin"] = get_origin(args.origin, 8 * 1024 - fileInfo["bankSize"])
        fileInfo["ignoreMask"] = 0b0000_0011

    fileInfo["ignoreMethod"] = args.ignore_method
    return fileInfo

# --------------------------------------------------------------------------------------------------

def read_file_slice(handle, bytesLeft):
    """Read a part of a file. Yield one chunk per call."""

    while bytesLeft > 0:
        chunkSize = min(bytesLeft, 2 ** 20)
        yield handle.read(chunkSize)
        bytesLeft -= chunkSize

def generate_blocks(handle, fileInfo):
    """Read the PRG ROM or the CHR ROM part from the CDL file.
    Notes: a "chunk" is a bufferful of unprocessed data; a "block" is a sequence of repeating bytes.
    yield: one block as (PRG_or_CHR_ROM_address, length, value) per call"""

    chunkStart = 0     # start address of current chunk
    blockStart = None  # start address of current block
    blockByte = None   # current repeating byte value

    byteFn = lambda b: int(bool(b)) if fileInfo["ignoreMethod"] else b & fileInfo["ignoreMask"]

    handle.seek(fileInfo["partStart"])
    for chunk in read_file_slice(handle, fileInfo["partSize"]):
        for (pos, byte) in enumerate(chunk):
            byte = byteFn(byte)
            if blockByte is None:
                # start new block
                blockStart = chunkStart + pos
                blockByte = byte
            elif byte != blockByte or (chunkStart + pos) % fileInfo["bankSize"] == 0:
                # end current block, start new one
                yield (blockStart, chunkStart + pos - blockStart, blockByte)
                blockStart = chunkStart + pos
                blockByte = byte
        # remember distance from the start of PRG/CHR ROM
        chunkStart += len(chunk)
    # end last block
    yield (blockStart, fileInfo["partSize"] - blockStart, blockByte)

# --------------------------------------------------------------------------------------------------

def PRG_byte_description(byte, args, bankSize):
    """Describe a PRG CDL byte. See http://www.fceux.com/web/help/fceux.html?CodeDataLogger.html"""

    if args.ignore_method:
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
    if byte and bankSize < 32 * 1024 and not args.ignore_bank:
        bankStart = 32 * 1024 + ((byte & 0b0000_1100) >> 2) * 8 * 1024
        items.append("last mapped to CPU bank 0x{:04x}-0x{:04x}".format(
            bankStart, bankStart + bankSize - 1
        ))
    return ", ".join(items) if items else "unaccessed"

def CHR_byte_description(byte, ignoreMethod):
    """Describe a CHR CDL byte."""

    if ignoreMethod and byte:
        return "accessed"
    if byte & 0b0000_0011 == 0b0000_0011:
        return "read programmatically & rendered"
    if byte & 0b0000_0010:
        return "read programmatically"
    if byte & 0b0000_0001:
        return "rendered"
    return "unaccessed"

def print_output(blocks, args, fileInfo):
    """Print the output."""

    for (addr, length, byte) in blocks:
        (bank, offset) = divmod(addr, fileInfo["bankSize"])
        NESAddr = fileInfo["origin"] + offset
        if args.part == "p":
            descr = PRG_byte_description(byte, args, fileInfo["bankSize"])
        else:
            descr = CHR_byte_description(byte, args.ignore_method)
        print(",".join(str(n) for n in (addr, bank, offset, NESAddr, length, byte, f'"{descr:s}"')))

# --------------------------------------------------------------------------------------------------

def main():
    """The main function."""

    args = parse_arguments()
    try:
        with open(args.input_file, "rb") as handle:
            fileInfo = get_file_info(handle, args)
            blocks = generate_blocks(handle, fileInfo)
            print_output(blocks, args, fileInfo)
    except OSError:
        sys.exit("Error reading the input file.")

if __name__ == "__main__":
    main()
