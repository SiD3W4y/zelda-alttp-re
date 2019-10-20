# Dialogs

Dialogs in the game are represented by printable character mixed with special opcodes
for formatting. There cannot be a null byte in the middle of a string except if it is
inside an opcode.

The address of the dialogs file is 0x8180ce8.

Whenever a piece of text is needed it is decrypted from the resources to a temporary
buffer.

## Opcode format

| Marker      | Opcode size          | Command               |
| :---------: | :------------------: | :-------------------: |
|  0x1a       | any 8 bit value >= 2 | opcode size - 2 bytes |
