# Dialogs

Dialogs in the game are represented by printable character mixed with special opcodes
for formatting. There cannot be a null byte in the middle of a string except if it is
inside an opcode.

The address of the dialogs file is 0x8180ce8.

Whenever a piece of text is needed it is decrypted from the resources to a temporary
buffer.

Using the ```resource_unpacker.py``` in scripts you can decrypt the resource file and
extract the various files inside. DAT1.bin is the file containing the dialogs for the
game. Using the ```dialog_dump.py``` you can do the conversion binary format <--> 
human editable format.

## Opcode format

| Marker      | Opcode size          | Command               |
| :---------: | :------------------: | :-------------------: |
|  0x1a       | any 8 bit value >= 2 | opcode size - 2 bytes |

## Opcodes
| Opcode | Size | Description 		      |
| :----: | :--: | :-------------------------: |
|  0x6a	 | 5	| Displays the player's name  |
|  0x7e  | 5	| Wait for keypress	      |
|  0x7f	 | 5	| End of current dialog box ? |
