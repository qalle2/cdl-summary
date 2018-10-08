import getopt
import os.path
import sys

PRG_BANK_SIZE = 16 * 1024
CHR_BANK_SIZE = 8 * 1024

PRG_PCM_DATA = 0b0100_0000
PRG_INDIRECT_DATA = 0b0010_0000
PRG_INDIRECT_CODE = 0b0001_0000
PRG_BANK = 0b0000_1100
PRG_DATA = 0b0000_0010
PRG_CODE = 0b0000_0001

CHR_READ = 0b0000_0010
CHR_DRAWN = 0b0000_0001

# maximum size of buffer when reading files, in bytes
FILE_BUFFER_MAX_SIZE = 2 ** 20

def parse_arguments():
    """Parse command line arguments using getopt."""

    longOpts = (
        "prg-rom-banks=",
        "part=",
        "output-format=",
        "omit-unaccessed",
        "ignore-method",
        "ignore-bank",
    )
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "b:p:o:", longOpts)
    except getopt.GetoptError:
        exit("Error: invalid option. See the readme file.")

    if len(args) != 1:
        exit("Error: invalid number of arguments. See the readme file.")

    opts = dict(opts)

    # PRG-ROM size
    prgBankCount = opts.get("--prg-rom-banks", opts.get("-b"))
    if prgBankCount is None:
        exit("Error: the PRG-ROM size argument is required.")
    try:
        prgBankCount = int(prgBankCount, 10)
        if not 1 <= prgBankCount <= 255:
            raise ValueError
    except ValueError:
        exit("Error: invalid number of PRG-ROM banks.")
    prgSize = prgBankCount * PRG_BANK_SIZE

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
    ignoreBank = "--ignore-bank" in opts

    # input file
    source = args[0]
    if not os.path.isfile(source):
        exit("Error: file not found.")
    sourceSize = os.path.getsize(source)

    # validate file size (one PRG bank equals two CHR banks)
    (bankCount, remainder) = divmod(sourceSize, CHR_BANK_SIZE)
    if not 2 <= bankCount <= 255 * 3 or remainder > 0:
        exit("Error: invalid file size.")

    # validate PRG size
    if prgSize > sourceSize:
        exit("Error: PRG-ROM size cannot be larger than file size.")

    # validate CHR-ROM size
    (chrBankCount, remainder) = divmod(sourceSize - prgSize, CHR_BANK_SIZE)
    if not 0 <= chrBankCount <= 255 or remainder > 0:
        exit(
            "Error: invalid CHR-ROM size (difference of file size and "
            "PRG-ROM size)."
        )
    if part == "C" and chrBankCount == 0:
        exit("Error: no CHR-ROM to read.")

    # get the start position and the length of PRG/CHR-ROM
    if part == "P":
        partStart = 0
        partLength = prgSize
    else:
        partStart = prgSize
        partLength = sourceSize - prgSize

    return {
        "part": part,
        "outputFormat": outputFormat,
        "omitUnaccessed": omitUnaccessed,
        "ignoreMethod": ignoreMethod,
        "ignoreBank": ignoreBank,
        "source": source,
        "partStart": partStart,
        "partLength": partLength,
    }

def read_file(handle, start, bytesLeft):
    """Yield a slice from a file in chunks."""

    handle.seek(start)
    while bytesLeft > 0:
        chunkSize = min(bytesLeft, FILE_BUFFER_MAX_SIZE)
        yield handle.read(chunkSize)
        bytesLeft -= chunkSize

def generate_repeating_bytes(handle, settings):
    """Read the PRG-ROM or the CHR-ROM from a CDL file.
    Yield the offset, length and value of each repeating byte."""

    repeatPos = None  # position of current repeating byte in file
    repeatByte = None  # current repeating byte value
    chunkStart = 0  # position of chunk in PRG/CHR-ROM

    if settings["part"] == "P":
        validationMask = 0b1000_0000
        ignoreMask = 0b1111_1111
        if settings["ignoreMethod"]:
            ignoreMask &= 0b1000_1111
        if settings["ignoreBank"]:
            ignoreMask &= 0b1111_0011
    else:
        validationMask = 0b1111_1100
        ignoreMask = 0b1111_1111

    # read PRG/CHR-ROM in chunks
    for chunk in read_file(
        handle, settings["partStart"], settings["partLength"]
    ):
        # loop through bytes in chunk
        for (pos, byte) in enumerate(chunk):
            # validate byte
            if byte & validationMask:
                exit("Error: invalid byte at 0x{:04x}: 0x{:02x}".format(
                    settings["partStart"] + chunkStart + pos, byte
                ))
            # ignore bits
            byte &= ignoreMask
            # start a new repeating byte if necessary
            if repeatByte is None or byte != repeatByte:
                if repeatByte is not None:
                    if repeatByte != 0x00 or not settings["omitUnaccessed"]:
                        length = chunkStart + pos - repeatPos
                        yield (repeatPos, length, repeatByte)
                repeatPos = chunkStart + pos
                repeatByte = byte
        # remember the distance from the start of PRG/CHR-ROM
        chunkStart += len(chunk)

    # the last repeating byte
    if repeatByte != 0x00 or not settings["omitUnaccessed"]:
        length = settings["partLength"] - repeatPos
        yield (repeatPos, length, repeatByte)

def format_byte_description(byte, settings):
    """Describe a CDL byte."""

    if byte == 0:
        return "unaccessed"

    items = []
    if settings["part"] == "P":
        # PRG-ROM log
        if byte & PRG_CODE:
            # code
            if byte & PRG_INDIRECT_CODE:
                items.append("code (indirectly accessed)")
            else:
                items.append("code")
        if byte & PRG_DATA:
            # data
            if byte & PRG_INDIRECT_DATA and byte & PRG_PCM_DATA:
                items.append("data (indirectly accessed & PCM audio)")
            elif byte & PRG_INDIRECT_DATA:
                items.append("data (indirectly accessed)")
            elif byte & PRG_PCM_DATA:
                items.append("data (PCM audio)")
            else:
                items.append("data")
        if not settings["ignoreBank"]:
            # bank
            bank = 0x8000 + ((byte >> 2) & 0b11) * 0x2000
            items.append("mapped to 0x{:04x}-0x{:04x}".format(
                bank, bank + 0x1fff
            ))
    else:
        # CHR-ROM log
        if byte & CHR_READ:
            items.append("read programmatically")
        if byte & CHR_DRAWN:
            items.append("rendered")

    return ", ".join(items)

def long_output(handle, settings):
    """Print output in long (human-readable) format."""

    print(
        "Start address (hexadecimal), end address (hexadecimal), length "
        "(decimal), description:"
    )

    maxAddrLen = len(format(settings["partLength"] - 1, "x"))
    maxRunLen = len(str(settings["partLength"]))
    lineFormat = (
        "{{:0{maxAddrLen:d}x}}-{{:0{maxAddrLen:d}x}}"
        " ({{:{maxRunLen:d}d}}):"
        " {{:s}}".format(maxAddrLen=maxAddrLen, maxRunLen=maxRunLen)
    )

    for (pos, length, byte) in generate_repeating_bytes(handle, settings):
        print(lineFormat.format(
            pos,
            pos + length - 1,
            length,
            format_byte_description(byte, settings)
        ))

def short_output(handle, settings):
    """Print output in short (CSV) format."""

    print('"start","length","byte"')
    for repeatByteData in generate_repeating_bytes(handle, settings):
        print(",".join(str(n) for n in repeatByteData))

def main():
    settings = parse_arguments()
    try:
        with open(settings["source"], "rb") as handle:
            if settings["outputFormat"] == "L":
                long_output(handle, settings)
            else:
                short_output(handle, settings)
    except OSError:
        exit("Error reading the file.")

if __name__ == "__main__":
    main()
