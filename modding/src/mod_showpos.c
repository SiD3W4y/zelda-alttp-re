#include <stdint.h>

#define X_POS_BUF 0x200b20a
#define Y_POS_BUF 0x200b216

static void itot(uint16_t, uint16_t*);

void showpos_entry(void)
{
    uint16_t link_x_pos = *(uint16_t*)0x30038f4;
    uint16_t link_y_pos = *(uint16_t*)0x30038f0;

    itot(link_x_pos, (uint16_t*)X_POS_BUF);
    itot(link_y_pos, (uint16_t*)Y_POS_BUF);
}

static void itot(uint16_t in, uint16_t* result)
{
    result = result + 3;

    for (int i = 0; i < 4; i++)
    {
        uint16_t num = in % 10;
        in /= 10;
        *result = 0x90 | num;
        result--;
    }
}
