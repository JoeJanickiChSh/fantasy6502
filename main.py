from py65emu.cpu import CPU
from py65emu.mmu import MMU

rawrom = []
with open('prog.bin', 'rb') as fp:
    byts = fp.read()
    for b in byts:
        rawrom.append(b)
mmu = MMU([
    (0x0000, 0x0500),
    (0x0600, 0xffff + 1 - 0x0600, True, rawrom)
])
cpu = CPU(mmu, 0x0600)
while not cpu.r.getFlag('B'):
    if mmu.read(0x0200):
        print(chr(mmu.read(0x0200)), end='')
        mmu.write(0x0200, 0)
    cpu.step()
