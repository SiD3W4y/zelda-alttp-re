.code 16
.section .text

.global _start
.type _start, %function

_start:
    # put the custom code for your trampoline here
    bl mod_entry

    # here we come from a patch at the end of the function 0x80c1b40
    # r4, r5 and r6 need to be popped after our hook
    pop {r4, r5, r6}
    pop {r0}
    bx r0
