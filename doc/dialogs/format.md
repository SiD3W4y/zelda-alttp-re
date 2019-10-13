# Dialogs

Dialogs in the game are represented by printable character mixed with special opcodes
for formatting. There cannot be a null byte in the middle of a string except if it is
inside an opcode.

## Opcode format

| Marker      | Opcode size          | Command               |
| :---------: | :------------------: | :-------------------: |
|  0x1a       | any 8 bit value >= 2 | opcode size - 2 bytes |
