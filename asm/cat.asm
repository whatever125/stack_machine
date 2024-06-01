; cat

section data:
    port:   1
section code:
    ; in >> len, out << len, halt if len == 0
    PUSH    port        ; [port]
    LOAD                ; [1]
    IN                  ; [len]
    DUP                 ; [len, len]
    PUSH    port        ; [len, len, port]
    LOAD                ; [len, len, 1]
    OUT                 ; [len]
    DUP                 ; [len, len]
    PUSH    break       ; [len, len, break]
    SWAP                ; [len, break, len]
    JZ                  ; [len]

loop:
    ; in >> chr, out << chr
    PUSH    port        ; [len, port]
    LOAD                ; [len, 1]
    IN                  ; [len, chr]
    PUSH    port        ; [len, chr, port]
    LOAD                ; [len, chr, 1]
    OUT                 ; [len]

    ; len--, halt if len == 0
    DEC                 ; [len--]
    DUP                 ; [len, len]
    PUSH    break       ; [len, len, break]
    SWAP                ; [len, break, len]
    JZ                  ; [len]

    ; loop
    PUSH    loop        ; [len, loop]
    JMP                 ; [len]
break:
    HALT