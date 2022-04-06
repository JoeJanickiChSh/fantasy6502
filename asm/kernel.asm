; Test of basic screen drawing, mouse, and keyboard

UPDATE = $03ff
SCREEN = $0400
KEYBOARD = $03fe
MOUSEX = $03fd
MOUSEY = $03fc
MOUSEDOWN = $03fb
; Layout:
; 0000-00ff User RAM
; 0100-01ff Stack
; 0200-02ff User RAM
; 0300-037F Kernel RAM
; 0380-03FF Hardware Registers
; 0400-04ff Screen RAM

STOREX = $0300
STOREY = $0301
STOREA = $0302


XPOS = $0000
YPOS = $0001
loop:
    jsr ClearScreen
    ldx MOUSEX
    stx XPOS
    lsr XPOS
    lsr XPOS
    lsr XPOS
    ldx XPOS
    ldy MOUSEY
    lda MOUSEDOWN
    ora #$AA
    jsr PlotPixel

    ldx #$07
    ldy #$1f
    lda KEYBOARD
    jsr PlotPixel

    jsr UpdateScreen
jmp loop

PlotPixel:
    stx STOREX
    sty STOREY
    sta STOREA
    asl STOREY
    asl STOREY
    asl STOREY
    lda STOREY
    adc STOREX
    tax
    lda STOREA
    sta SCREEN, x
    rts


ClearScreen:
    ldx #$00
    lda #$00
    ClearLoop:
        sta SCREEN, x
        inx
        cpx #$00
        bne ClearLoop
    rts

UpdateScreen:
    lda #$01
    sta UPDATE
    rts

