import argparse
import sqlite3


def write_db(infile, outfile):
    db = sqlite3.connect(outfile)
    c = db.cursor()

    # Create tables required by wakare frontends
    c.execute("CREATE TABLE branches (step INTEGER NOT NULL PRIMARY KEY, type INTEGER, source INTEGER, destination INTEGER);")
    c.execute("CREATE TABLE mappings (id INTEGER NOT NULL PRIMARY KEY, filename TEXT, start INTEGER, end INTEGER);")
    c.execute("CREATE TABLE hitcounts (id INTEGER NOT NULL PRIMARY KEY, address INTEGER, hitcount INTEGER);")

    # Insert gba mappings
    c.execute("INSERT INTO mappings (id, filename, start, end) VALUES (?, ?, ?, ?);",
              (0, "ROM", 0x08000000, 0x0a000000))

    fd = open(infile, "r")
    sid = 1

    for l in fd.readlines():
        l = l.strip()

        if len(l) == 0:
            continue

        chks = l.split(" ")

        if len(chks) != 2:
            print("Invalid format")
            break

        addr = int(chks[0], 16)
        count = int(chks[1])

        if addr < 0x08000000:
            print("Invalid address: 0x{:08x}".format(addr))
            continue

        c.execute("INSERT INTO hitcounts (id, address, hitcount) VALUES (?, ?, ?);",
                (sid, addr, count))
        sid += 1

    db.commit()
    db.close()

def main():
    parser = argparse.ArgumentParser(description="mgba basic block coverage trace to wakare database converter")
    parser.add_argument("-i", "--input", help="Input trace from mgba")
    parser.add_argument("-o", "--output", help="Output wakare sqlite database")
    args = parser.parse_args()

    if not args.input:
        print("Please specify an input file")
        return

    if not args.output:
        args.output = "trace.db"

    write_db(args.input, args.output)

if __name__ == '__main__':
    main()
