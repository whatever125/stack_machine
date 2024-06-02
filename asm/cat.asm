; cat

section data:
    port:   1
section code:
    ; in >> len, out << len, halt if len == 0
    push    port        ; [port]
    load                ; [1]
    in                  ; [len]
    dup                 ; [len, len]
    push    port        ; [len, len, port]
    load                ; [len, len, 1]
    out                 ; [len]
    dup                 ; [len, len]
    push    break       ; [len, len, break]
    swap                ; [len, break, len]
    jz                  ; [len]

loop:
    ; in >> chr, out << chr
    push    port        ; [len, port]
    load                ; [len, 1]
    in                  ; [len, chr]
    push    port        ; [len, chr, port]
    load                ; [len, chr, 1]
    out                 ; [len]

    ; len--, halt if len == 0
    dec                 ; [len--]
    dup                 ; [len, len]
    push    break       ; [len, len, break]
    swap                ; [len, break, len]
    jz                  ; [len]

    ; loop
    push    loop        ; [len, loop]
    jmp                 ; [len]
break:
    halt