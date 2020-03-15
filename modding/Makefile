CC=arm-none-eabi-gcc
CFLAGS=-mthumb -ffreestanding -nostdlib -nostartfiles -nodefaultlibs -fPIC
LDFLAGS=-static -nostartfiles
OBJS= src/entry.o \
	  src/main.o \
	  src/mod_showpos.o

.PHONY: clean

mod.bin: mod.elf
	python modcheck.py

mod.elf: $(OBJS)
	$(CC) $(LDFLAGS) $^ -o $@

clean:
	$(RM) $(OBJS)
	$(RM) mod.elf
	$(RM) mod.bin
