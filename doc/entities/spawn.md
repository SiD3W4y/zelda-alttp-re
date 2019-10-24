# Spawn

The spawn information about entities is stored in an array. This array is stored at
address 0x82293f0 and has the following format.

| Packed Y coordinate / Special entity marker | Packed X coordinate | Entity id |
| :-----------------: | :-----------------: | :-------: |
| u8                  | u8                  | u8        |

These entries are stored contiguously and are separated by an end of stream marker
(if entity Y coordinate is 0xff then there is no more entity to load). A group entry
also starts by a NULL byte. We thus have the following format:

```
[0x00][0 or more entries][0xff]
```

## Packed coordinates
Both X and Y coordinates are stored in a packed manner. Entities in the game have their
position stored into two separate u8 arrays for each of their coordinates (high and
low byte of a u16). The packed bytes do no represent an absolute position but are offsets
added to the current map position.

We can compute the low coordinate byte as such:

```
pos_low_byte = (pos_packed & 0xf) << 4
```
