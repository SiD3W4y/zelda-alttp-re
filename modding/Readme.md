# Modding GBA games using C

Writing small patches for games is fun and easy, but quickly gets quite limited.
This example project is a demonstration on how to have a "sane" setup for GBA game
modding. The goal is to have as little handwritten assembly as possible and only use
it as glue code for our C mods.

## Possible issues
### Linking order

We want our entrypoint to be at the offset 0 of the text section as it will be easier
during the patching process, much like a shellcode. It means that the linking order of
the objects is critical and that the object containing *_start* should always be the
first argument of the linker.


## Restrictions

As the code will be extracted and written in the ROM region, it is not possible to have
a writable section easily. It can be implemented using a custom linker script.

The ROM is immutable and thus it is not possible to use a patch -> restore -> repatch
methodology as used in classic hooking.

## Structure
### src/entry.S
Used as the entrypoint to our mod. It is used to reimplement the behavior of the instructions
overwriten by our hook. We cannot simply write them back as the ROM is immutable.

### src/main.c
Main of our mod, implement your stuff here.

### modcheck.py
Used in the compilation pipeline to check that the raw machine code can be safely extracted from
the compiled object file.

# Example: Position display for Link to the Past

The code we patch to call our mod is a such:

```asm
080c1d28  70bc pop {r4, r5, r6}
080c1d2a  01bc pop {r0}
080c1d2c  0047 bx r0
080c1d2e  0000 <padding>
```

It is the epilogue one of the functions updating npc stats every frame (0x80c1b40). We will
replace this code by a jump to our mod code wich will be loaded at address 0x08700000.

```asm
080c1d28 0048 ldr r0, [0x080c1d2c]
080c1d2a 0047 bx r0
080c1d2c 01007008 <mode_code_addr: 0x08700001>
```

Here the address for the jump ends with one to indicate to the cpu that the target of the jump
is thumb code and not arm code.
As our patch overwrote the three last instructions of the function we will reimplement them in
entry.S as such.

```asm
_start:
	bl mod_entry

	pop {r4, r5, r6}
	pop {r0}
	bx r0
```

Then just write the mod.bin file to the correct address and the hook is done.
