#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL
# was not distributed with this file, You can obtain
# one at https://mozilla.org/MPL/2.0/.

import sys

print("MS Paint file converter utility v0.1")
print("Written by A.M. Rowsell, MPL Version 2.0 license\n")
if len(sys.argv) < 2:
    print("Please provide filename (without extension)!")
    print("Example usage:\n./mspconvert.py DONUT")
    sys.exit(255)

filename = sys.argv[1]
width = 0
height = 0
# The output file follows the very simple XBM format
# which is just a basic C syntax array variable
outputString = '''
#define {0}_width {1}
#define {0}_height {2}
static unsigned char {0}_bits [] =
'''

# Output data starts as an empty bytearray
outputData = b''

try:
    with open(filename + ".MSP", 'rb') as f:
        versionString = f.read(4)
        if versionString == b'\x4c\x69\x6e\x53':
            version = 2
        elif versionString == b'\x44\x61\x6e\x4d':
            version = 1
        else:
            print("The given file {0}.MSP is not a valid Microsoft Paint file!".format(filename))
            sys.exit(255)

        if version == 2:
            print("Version 2 Paint file detected...")
            width = int.from_bytes(f.read(2), "little")
            height = int.from_bytes(f.read(2), "little")
            size = int((width * height) / 8)
            f.seek((height * 2) + 32) # seek to the start of image data
            while(byte := f.read(1)):
                if(int.from_bytes(byte, "little") == 0): # RLL-encoded
                    rllLen = int.from_bytes(f.read(1), "little")
                    rllValue = f.read(1)
                    for i in range(0,rllLen):
                        outputData += rllValue
                        size -= 1
                else:
                    rllLen = int.from_bytes(byte, "little")
                    for i in range(0,rllLen):
                        outputData += f.read(1)
                        size -= 1
                        print("Remaining size: {0}".format(size))
            for i in range(0, size):
                outputData += b'\xff'

            with open(filename + "_converted.xbm", 'w') as f:
                print("Writing output file...")
                f.write(outputString.format(filename, width, height))
                f.write(" {")
                q = 0
                for byte in outputData:
                    result = int('{:08b}'.format(byte)[::-1], 2)
                    f.write("0x" + '{:x}'.format(result) + ", ")
                    q += 1
                    if q >= 16:
                        f.write("\n")
                        q = 0
                        f.write(" };")
                        print("Done!")
                        sys.exit(0)
        elif version == 1:
            print("Version 1 Paint detected...")
            width = int.from_bytes(f.read(2), "little")
            height = int.from_bytes(f.read(2), "little")
            f.seek(28)
            q = 0
            outputString = outputString.format(filename, width, height)
            outputString += " {\n"
            while(byte := f.read(1)):
                result = int('{:08b}'.format(int.from_bytes(byte, "big"))[::-1], 2)
                outputString += "0x" + '{:x}'.format(result) + ", "
                q += 1
                if q >= 16:
                    outputString += "\n"
                    q = 0
                    outputString += " };"

            with open(filename + "_converted.xbm", 'w') as f:
                print("Writing output file...")
                f.write(outputString)
                print("Done!")
                sys.exit(0)
except FileNotFoundError:
    print("{0}.MSP does not exist! Quitting...".format(filename))
    sys.exit(255)
except PermissionError:
    print("Unable to open {0}.MSP -- insufficient permissions! Quitting...".format(filename))
    sys.exit(255)
except Exception:
    print("Something went wrong! Quitting...")
    sys.exit(255)


