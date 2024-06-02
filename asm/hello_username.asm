; hello_username

section data:
    port:       1
    question:   "What is your name? "
    hello:      "Hello, "
    username:   bf  32

section code:
    push    question    ; [question_addr]
    push    print_str   ; [question_addr, print_str_addr]
    call                ; []
    push    username    ; [username_addr]
    push    read_str    ; [username_addr, read_str_addr]
    call                ; []
    push    hello       ; [hello_addr]
    push    print_str   ; [hello_addr, print_str_addr]
    call                ; []
    push    username    ; [username_addr]
    push    print_str   ; [username_addr, print_str_addr]
    call                ; []
    halt

print_char: ; (chr)
    push    port        ; [chr, port_addr]
    load                ; [chr, port]
    out                 ; []
    ret

print_str:  ; (addr)
    dup                 ; [addr, addr]
    load                ; [addr, len]
    dup                 ; [addr, len, len]
    push    print_char  ; [addr, len, len, print_char_addr]
    call                ; [addr, len]
    dup                 ; [addr, len, len]
    push    ps_break    ; [addr, len, len, ps_break]
    swap                ; [addr, len, ps_break, len]
    jz                  ; [addr, len]
    swap                ; [len, addr]
ps_loop:
    inc                 ; [len, ++addr]
    dup                 ; [len, addr, addr]
    load                ; [len, addr, chr]
    push    print_char  ; [len, addr, chr, print_char_addr]
    call                ; [len, addr]

    swap                ; [addr, len]
    dec                 ; [addr, --len]
    dup                 ; [addr, len, len]
    push    ps_break    ; [addr, len, len, ps_break]
    swap                ; [addr, len, ps_break, len]
    jz                  ; [addr, len]

    swap                ; [len, addr]
    push    ps_loop     ; [len, addr, ps_loop_addr]
    jmp                 ; [len, addr]
ps_break:
    pop                 ; [len]
    pop                 ; []
    ret

read_char:  ; ()
    push    port        ; [port_addr]
    load                ; [port]
    in                  ; [chr]
    ret

read_str:   ; (addr)
    dup                 ; [addr, addr]
    push    read_char   ; [addr, addr, read_char_addr]
    call                ; [addr, addr, len]
    over                ; [addr, len, addr, len]
    swap                ; [addr, len, len, addr]
    save                ; [addr, len]
    dup                 ; [addr, len, len]
    push    rs_break    ; [addr, len, len, rs_break]
    swap                ; [addr, len, rs_break, len]
    jz                  ; [addr, len]
rs_loop:
    swap                ; [len, addr]
    inc                 ; [len, ++addr]
    dup                 ; [len, addr, addr]
    push    read_char   ; [len, addr, addr, read_char_addr]
    call                ; [len, addr, addr, chr]
    swap                ; [len, addr, chr, addr]
    save                ; [len, addr]
    swap                ; [addr, len]
    dec                 ; [addr, --len]
    dup                 ; [addr, len, len]
    push    rs_break    ; [addr, len, len, rs_break]
    swap                ; [addr, len, rs_break, len]
    jz                  ; [addr, len]

    push    rs_loop     ; [addr, len, rs_loop_addr]
    jmp                 ; [addr, len]
rs_break:
    pop                 ; [addr]
    pop                 ; []
    ret
