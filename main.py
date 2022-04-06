from py65emu.cpu import CPU
from py65emu.mmu import MMU
import pygame as pg


pg.init()

VIDEO_REGISTER = 0x0400
VIDEO_UPDATE_REGISTER = 0x03ff
KEYBOARD_REGISTER = 0x03fe
MOUSEX_REGISTER = 0x03fd
MOUSEY_REGISTER = 0x03fc
MOUSEDOWN_REGISTER = 0x03fb


def main():
    window = pg.display.set_mode((64*8, 32 * 8))
    d = pg.Surface((64, 32))
    rawrom = []
    with open('kernel.bin', 'rb') as fp:
        byts = fp.read()
        for b in byts:
            rawrom.append(b)
    mmu = MMU([
        (0x0000, 0x0500),
        (0x0600, 0xffff + 1 - 0x0600, True, rawrom)
    ])
    cpu = CPU(mmu, 0x0600)
    while not cpu.r.getFlag('B'):
        update = mmu.read(VIDEO_UPDATE_REGISTER)
        if update:
            mmu.write(VIDEO_UPDATE_REGISTER, 0)
            d.fill((0, 0, 0))
            for y in range(32):
                for x in range(64):
                    x_byte = x // 8
                    x_bit = 7 - (x % 8)
                    in_byte = mmu.read(VIDEO_REGISTER + x_byte + y * 8)
                    if in_byte & (1 << x_bit):
                        d.set_at((x, y), (255, 255, 255))

            window.blit(pg.transform.scale(d, (64*8, 32*8)), (0, 0))

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif e.type == pg.KEYDOWN:
                    mmu.write(KEYBOARD_REGISTER, e.key & 0xff)
                elif e.type == pg.KEYUP:
                    mmu.write(KEYBOARD_REGISTER, 0)

            mmu.write(MOUSEX_REGISTER, pg.mouse.get_pos()[0] // 8)
            mmu.write(MOUSEY_REGISTER, pg.mouse.get_pos()[1] // 8)
            mmu.write(MOUSEDOWN_REGISTER,
                      0xff if pg.mouse.get_pressed()[0] else 0x00)
            pg.display.update()
        cpu.step()


if __name__ == '__main__':
    main()
