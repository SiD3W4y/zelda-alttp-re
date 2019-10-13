import argparse
import struct

RESOURCES_KEY = b"l0ZxE8SjYv3#RhaX"


def u32be(d):
    return struct.unpack(">I", d)[0]


def to_u32(n):
    if n > 0:
        return n & 0xffffffff

    return ((-n ^ 0xffffffff) + 1) & 0xffffffff


def decrypt_resources(infd, outfd):
    data = bytearray(infd.read())
    out = bytearray(len(data))
    key = bytearray(RESOURCES_KEY)

    for i in range(len(data)):
        xor_k1 = key[i & 0xf]
        xor_k2 = to_u32((i & 0xff) - key[15 - (i & 0xf)])

        if i > 0x2a:
            res = to_u32((data[i] ^ xor_k2) - data[i - 0x2b])
        else:
            res = data[i] ^ xor_k2

        res = to_u32(res - (i & 0xff)) ^ xor_k1
        out[i] = res & 0xff

    outfd.write(out)


def encrypt_resources(infd, outfd):
    data = bytearray(infd.read())
    out = bytearray(len(data))
    key = bytearray(RESOURCES_KEY)

    for i in range(len(data)):
        xor_k1 = key[i & 0xf]
        xor_k2 = to_u32((i & 0xff) - key[15 - (i & 0xf)])
        res = to_u32((data[i] ^ xor_k1) + (i & 0xff))

        if i > 0x2a:
            res = to_u32(res + out[i - 0x2b]) ^ xor_k2
        else:
            res ^= xor_k2

        out[i] = res & 0xff

    outfd.write(out)


def extract_resources(infd):
    header = infd.read(32)

    if len(header) != 32:
        raise Exception("Truncated global header")

    entry_count = u32be(header[0xc:0x10])
    print("Extracting {} files".format(entry_count))

    for i in range(entry_count):
        header = infd.read(16)

        if len(header) != 16:
            raise Exception("Truncated entry header")

        name = str(header[0:4], "UTF-8")
        size = u32be(header[4:8])
        data_size = size - len(header)

        print("Extracting {} to {}.bin (size {} bytes)".format(name, name, data_size))
        data = infd.read(data_size)

        if len(data) != data_size:
            raise Exception("Truncated file content")

        open("{}.bin".format(name), "wb").write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="Specifies the mode of operation (encrypt/decrypt/extract)", default="extract")
    parser.add_argument("-i", "--input", help="Specifies the input file", default="resources.in")
    parser.add_argument("-o", "--output", help="Specifies the output file", default="resources.out")
    args = parser.parse_args()

    infd = open(args.input, "rb")

    if args.mode == "extract":
        extract_resources(infd)
    elif args.mode == "decrypt":
        outfd = open(args.output, "wb")
        decrypt_resources(infd, outfd)
    elif args.mode == "encrypt":
        outfd = open(args.output, "wb")
        encrypt_resources(infd, outfd)
    else:
        print("Mode '{}' is invalid".format(args.mode))
