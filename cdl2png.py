import itertools, os, sys
from PIL import Image  # Pillow, https://python-pillow.org

# 2 LSBs of CDL byte -> RGB color;
# see http://fceux.com/web/help/CodeDataLogger.html
OUTPUT_PALETTE = (
    (0x00, 0x00, 0x00),  # 0b00: unaccessed
    (0xff, 0x80, 0x00),  # 0b01: code (PRG) / rendered (CHR)
    (0x00, 0x80, 0xff),  # 0b10: data (PRG) / read programmatically (CHR)
    (0xff, 0xff, 0xff),  # 0b11: both
)

def parse_arguments():
    # return (name of input file, name of output file)

    if len(sys.argv) != 3:
        sys.exit(
            "Convert an FCEUX Code/Data Logger file (.cdl) into a PNG image "
            "file. Arguments: inputFile outputFile. See README.md for details."
        )

    (inFile, outFile) = sys.argv[1:]

    if not os.path.isfile(inFile):
        sys.exit("Input file not found.")
    try:
        fileSize = os.path.getsize(inFile)
    except OSError:
        sys.exit("Error getting input file size.")
    if fileSize == 0 or fileSize % 256 > 0:
        sys.exit("Input file size must be a multiple of 256 bytes.")

    if os.path.exists(outFile):
        sys.exit("Output file already exists.")

    return (inFile, outFile)

def create_image(handle):
    # read CDL data from file, return indexed image

    dataLen = handle.seek(0, 2)
    image = Image.new("P", (256, dataLen // 256))
    image.putpalette(itertools.chain.from_iterable(OUTPUT_PALETTE))
    handle.seek(0)
    image.putdata(tuple(b & 0b11 for b in handle.read()))
    return image

def main():
    (inFile, outFile) = parse_arguments()

    try:
        with open(inFile, "rb") as handle:
            image = create_image(handle)
    except OSError:
        sys.exit("Error reading input file.")

    try:
        with open(outFile, "wb") as handle:
            handle.seek(0)
            image.save(handle, "png")
    except OSError:
        sys.exit("Error writing output file.")

main()
