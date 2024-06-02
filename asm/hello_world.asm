; hello_world

section data:
    port:   1
    hello:  "Hello, world!"

section code:
    ; out << len, halt if len == 0
    push    hello       ; [hello_addr]
    load                ; [len]
    dup                 ; [len, len]
    push    port        ; [len, len, port_addr]
    load                ; [len, len, port]
    out                 ; [len]
    dup                 ; [len, len]
    push    break       ; [len, len, break]
    swap                ; [len, break, len]
    jz                  ; [len]
    push    hello       ; [len, hello_addr]

loop:
    ; out << chr
    inc                 ; [len, hello_addr++]
    dup                 ; [len, hello_addr, hello_addr]
    load                ; [len, hello_addr, chr]
    push    port        ; [len, hello_addr, chr, port_addr]
    load                ; [len, hello_addr, chr, port]
    out                 ; [len, hello_addr]

    ; len--, halt if len == 0
    swap                ; [hello_addr, len]
    dec                 ; [hello_addr, len--]
    dup                 ; [hello_addr, len, len]
    push    break       ; [hello_addr, len, len, break]
    swap                ; [hello_addr, len, break, len]
    jz                  ; [hello_addr, len]

    ; loop
    swap                ; [len, hello_addr]
    push    loop        ; [len, hello_addr, loop_addr]
    jmp                 ; [len, hello_addr]
break:
    halt