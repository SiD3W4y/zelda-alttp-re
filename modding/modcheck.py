import r2pipe
import sys

if __name__ == '__main__':
    r2 = r2pipe.open("./mod.elf")
    maps = r2.cmdJ("omj")

    # Checking map count
    if len(maps) != 1:
        print(f"[E] Found more maps than the expected .text (len {len(maps)})")
        sys.exit(1)

    perm = maps[0].perm

    # Checking map permission
    if perm != "r-x":
        print(f"[E] Wrong permission for segment, got '{perm}' expected 'r-x'")
        sys.exit(1)

    # Now checking that the entry point is at the beginning of the .text
    sections = r2.cmdJ("iSj")
    section = list(filter(lambda s: s.name == ".text", sections))

    if len(section) != 1:
        print("[E] Could not find '.text' section")
        sys.exit(1)

    section = section[0]
    entrypoints = r2.cmdJ("iej")

    if len(entrypoints) != 1:
        print("[E] Could not find entrypoint")
        sys.exit(1)

    entrypoint = entrypoints[0]

    if entrypoint.vaddr != section.vaddr:
        print(f"[E] Entrypoint mismatch: (section at 0x{section.vaddr:08x}, entry at 0x{entrypoint.vaddr:08x}")
        sys.exit(1)

    # Now dumping .text
    r2.cmd("s section..text")
    r2.cmd(f"wtf mod.bin {section.size}")
