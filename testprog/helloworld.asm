lda #$00
ldx #$00
loop:
    lda text, x
    sta $0200
    inx
    cmp #$00
    bne loop

text:
    .byte "hello, world!", 10, 0