# Global variables offsets

| Offset | Type | Content |
| :----: | :--: | :-----: |
| 0x200234d | u8 | Hearts (1 heart = 8 in value) |
| 0x200234c | u8 | Heart containers (max = 0xa0) |
| 0x200234e | u8 | Current magic (max = 0x80) |
| 0x2002340 | u16 | Rupees |
| 0x2002323 | u8 | Bombs |
| 0x2002357 | u8 | Arrows |
| 0x30038f0 | u16 | Link y pos (0) |
| 0x30038f4 | u16 | Link x pos (0) |
| 0x3003102 | u8[16] | Entity y - low byte |
| 0x3003112 | u8[16] | Entity x - low byte |
| 0x3003122 | u8[16] | Entity y - high byte |
| 0x3003132 | u8[16] | Entity x - high byte |
| 0x3003222 | u8[16] | Entity type array |
| 0x3003252 | u8[16] | Entity hp |
| 0x3003095 | u8[16] | Entity map id |
| 0x8228df0 | u32[384] | map id <-> spawn list array |
| 0x82293f0 | u8[] | Spawn list entries (see docs/entities/spawn.md) |
| 0x822769d | u8[] | map entity id <-> hp |
