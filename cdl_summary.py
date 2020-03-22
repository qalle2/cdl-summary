"""Print an FCEUX Code/Data Logger file (.cdl) in human-readable format."""

import argparse
import os
import sys

def parse_arguments():
    """Parse command line arguments using argparse."""

    parser = argparse.ArgumentParser(
        description="Print an FCEUX Code/Data Logger file (.cdl) in human-readable format. All "
        "options are required."
    )

    parser.add_argument(
        "-r", "--prg-size", type=int, required=True,
        help="The PRG ROM size of the input file, in KiB (16-4096 and a multiple of 16, usually a "
        "power of two)."
    )
    parser.add_argument(
        "-p", "--part", choices=("p", "c"), required=True,
        help="Which part to read from the input file. p=PRG ROM (default), c=CHR ROM."
    )
    parser.add_argument(
        "-o", "--origin", type=int, choices=(0, 1, 2, 3, 4, 5, 6, 7, 32, 40, 48, 56), required=True,
        help="The CPU/PPU address each ROM bank starts from, in KiB. 32/40/48/56 for PRG ROM, 0-7 "
        "for CHR ROM."
    )
    parser.add_argument(
        "-b", "--bank-size", type=int, choices=(1, 2, 4, 8, 16, 32), required=True,
        help="Size of PRG/CHR ROM banks in KiB. 8/16/32 for PRG ROM, 1/2/4/8 for CHR ROM. -o plus "
        "-b must be 64 or less for PRG ROM and 8 or less for CHR ROM."
    )
    parser.add_argument(
        "input_file", help="The .cdl file to read. Size: 16-6136 KiB and a multiple of 8 KiB."
    )

    args = parser.parse_args()

    # input file
    if not os.path.isfile(args.input_file):
        sys.exit("Input file not found.")

    # PRG ROM size
    if args.prg_size % 16:
        sys.exit("The specified PRG ROM size is not a multiple of 16.")
    if args.prg_size < 16:
        sys.exit("The specified PRG ROM size is too small.")
    if args.prg_size > 256 * 16:
        sys.exit("The specified PRG ROM size is too large.")

    # origin
    if args.part == "p" and args.origin < 32:
        sys.exit("Invalid CPU origin address.")
    if args.part == "c" and args.origin > 7:
        sys.exit("Invalid PPU origin address.")

    # ROM bank size
    if args.part == "p" and args.bank_size < 8:
        sys.exit("Invalid PRG ROM bank size.")
    if args.part == "c" and args.bank_size > 8:
        sys.exit("Invalid CHR ROM bank size.")

    return args

def get_file_size(handle):
    """Get the size of the input file."""

    fileSize = handle.seek(0, 2)
    if fileSize % (8 * 1024):
        sys.exit("The input file size is not a multiple of 8 KiB.")
    if fileSize < 16 * 1024:
        sys.exit("The input file is too small.")
    if fileSize > (256 * 16 + 255 * 8) * 1024:
        sys.exit("The input file is too large.")
    return fileSize

def get_file_info(args, fileSize):
    """Get more info on what to do based on args and file size."""

    # PRG ROM size
    PRGSize = args.prg_size * 1024
    if PRGSize > fileSize:
        sys.exit("The specified PRG ROM size is larger than the input file size.")
    if fileSize - PRGSize > 255 * 8 * 1024:
        sys.exit("The specified PRG ROM size would leave too large a CHR ROM.")

    # which addresses to read from the file
    partStart = 0 if args.part == "p" else PRGSize
    partSize = PRGSize if args.part == "p" else fileSize - PRGSize
    if args.part == "c" and partSize == 0:
        sys.exit("No CHR ROM (the file is all PRG ROM).")

    # CPU/PPU origin address
    origin = args.origin * 1024

    # PRG/CHR ROM bank size
    bankSize = args.bank_size * 1024
    if args.part == "p" and PRGSize % bankSize:
        sys.exit("Total PRG ROM size must be a multiple of PRG ROM bank size.")

    # sum of origin and bank size
    if args.part == "p" and origin + bankSize > 64 * 1024:
        sys.exit("The sum of CPU address origin and PRG ROM bank size is too large.")
    if args.part == "c" and origin + bankSize > 8 * 1024:
        sys.exit("The sum of PPU address origin and CHR ROM bank size is too large.")

    # the "ignore bitmask" (which value to AND all CDL bytes with)
    if args.part == "c":
        ignoreMask = 0b0000_0011  # only ignore the undefined bits
    elif args.bank_size == 8:
        ignoreMask = 0b0111_1111  # only ignore the undefined bit
    elif args.bank_size == 16:
        ignoreMask = 0b0111_1011  # ignore lower CPU bank bit
    else:
        ignoreMask = 0b0111_0011  # ignore both CPU bank bits

    return {
        "partStart": partStart,
        "partSize": partSize,
        "origin": origin,
        "bankSize": bankSize,
        "ignoreMask": ignoreMask,
    }

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

    handle.seek(fileInfo["partStart"])
    for chunk in read_file_slice(handle, fileInfo["partSize"]):
        for (pos, byte) in enumerate(chunk):
            byte &= fileInfo["ignoreMask"]
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

def PRG_byte_description(byte, omitBank, bankSize):
    """Describe a PRG CDL byte. See http://www.fceux.com/web/help/fceux.html?CodeDataLogger.html"""

    items = []
    if byte & 0b0000_0001:
        # code
        if byte & 0b0001_0000:
            items.append("code (indirectly accessed)")
        else:
            items.append("code")
    if byte & 0b0000_0010:
        # data
        if byte & 0b0010_0000 and byte & 0b0100_0000:
            items.append("data (indirectly accessed & PCM audio)")
        elif byte & 0b0010_0000:
            items.append("data (indirectly accessed)")
        elif byte & 0b0100_0000:
            items.append("data (PCM audio)")
        else:
            items.append("data")
    # CPU bank (only for accessed bytes)
    if byte and not omitBank:
        bankStart = (32 + ((byte & 0b0000_1100) >> 2) * 8) * 1024
        items.append("last mapped to CPU bank 0x{:04x}-0x{:04x}".format(
            bankStart, bankStart + bankSize - 1
        ))
    return ", ".join(items) if items else "unaccessed"

def CHR_byte_description(byte):
    """Describe a CHR CDL byte."""

    if byte & 0b0000_0010 and byte & 0b0000_0001:
        return "read programmatically & rendered"
    if byte & 0b0000_0010:
        return "read programmatically"
    if byte & 0b0000_0001:
        return "rendered"
    return "unaccessed"

def print_output(blocks, part, fileInfo):
    """Print the output."""

    fields = (
        "PRG address" if part == "p" else "CHR address",
        "CPU bank" if part == "p" else "PPU bank",
        "offset in bank",
        "CPU address" if part == "p" else "PPU address",
        "block length",
        "CDL byte",
        "description"
    )
    print(",".join(f'"{field:s}"' for field in fields))

    if part == "p":
        # CPU bank info is redundant if CPU bank size is 32 KiB or there is only one CPU bank
        omitCPUBank = fileInfo["bankSize"] in (32 * 1024, fileInfo["partSize"])

    for (addr, length, byte) in blocks:
        (bank, offset) = divmod(addr, fileInfo["bankSize"])
        NESAddr = fileInfo["origin"] + offset
        if part == "p":
            descr = PRG_byte_description(byte, omitCPUBank, fileInfo["bankSize"])
        else:
            descr = CHR_byte_description(byte)
        print(",".join(str(n) for n in (addr, bank, offset, NESAddr, length, byte, f'"{descr:s}"')))

def main():
    """The main function."""

    args = parse_arguments()
    try:
        with open(args.input_file, "rb") as handle:
            fileSize = get_file_size(handle)
            fileInfo = get_file_info(args, fileSize)
            blocks = generate_blocks(handle, fileInfo)
            print_output(blocks, args.part, fileInfo)
    except OSError:
        sys.exit("Error reading the input file.")

if __name__ == "__main__":
    main()
