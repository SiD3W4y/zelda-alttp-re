import sys
import argparse
import struct
import string
import binascii
import io


def disassemble_dialogs(fd):
    d = fd.read(1)
    res = io.StringIO()

    while len(d) == 1:
        op = struct.unpack("B", d)[0]

        if op == 0x1a:
            op_sz = struct.unpack("B", fd.read(1))[0] - 2
            op_data = fd.read(op_sz)
            res.write(f"#OP[{binascii.hexlify(op_data).decode()}]")
        elif chr(op) not in string.printable:
            res.write(f"#SP[{binascii.hexlify(d).decode()}]")
        else:
            res.write(d.decode())

        d = fd.read(1)

    return res.getvalue()


def assemble_dialogs(fd):
    res = io.BytesIO()
    d = fd.read(1)

    while len(d) == 1:
        if d == b"#":
            cmd = fd.read(2).decode()  # We don't check for any errors, yolo
            fd.read(1)  # Consume '['
            ops = b""

            while True:
                opb = fd.read(1)

                if opb == b"]":
                    break

                ops += opb

            op_data = binascii.unhexlify(ops.decode())

            if cmd == "OP":
                res.write(b"\x1a")
                res.write(struct.pack("B", len(op_data) + 2))
                res.write(op_data)
            else:
                res.write(op_data)
        else:
            res.write(d)

        d = fd.read(1)

    return res.getvalue()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Specifies input dialog file",
                        default="DAT1.bin")
    parser.add_argument("-o", "--output", help="Specifies output dialog file",
                        default="file.out")
    parser.add_argument("-m", "--mode",
                        help="File processing mode (disassemble/assemble)",
                        default="disassemble")

    args = parser.parse_args()
    infd = open(args.input, "rb")

    if args.mode not in ["disassemble", "assemble"]:
        print(f"Invalid mode {args.mode}")
        sys.exit(1)

    if args.mode == "disassemble":
        oufd = open(args.output, "w")
        oufd.write(disassemble_dialogs(infd))
        oufd.close()

    if args.mode == "assemble":
        oufd = open(args.output, "wb")
        oufd.write(assemble_dialogs(infd))
        oufd.close()

    infd.close()
