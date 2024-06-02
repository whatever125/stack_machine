section data:
    port:   1
    result: 0
section code:
start:
    push    1000    ; [i]
loop:
    dec             ; [--i]
    dup             ; [i, i]
    push    break   ; [i, i, break_addr]
    swap            ; [i, break_addr, i]
    jz              ; [i]

    dup             ; [i, i]

    dup             ; [i, i, i]
    push    3       ; [i, i, i, 3]
    swap            ; [i, i, 3, i]
    mod             ; [i, i, mod]
    push    suc     ; [i, i, mod, suc_addr]
    swap            ; [i, i, suc_addr, mod]
    jz              ; [i, i]

    dup             ; [i, i, i]
    push    5       ; [i, i, i, 5]
    swap            ; [i, i, 5, i]
    mod             ; [i, i, mod]
    push    suc     ; [i, i, mod, suc_addr]
    swap            ; [i, i, suc_addr, mod]
    jz              ; [i, i]

    pop             ; [i]
    push    loop    ; [i, loop_addr]
    jmp             ; [i]

suc:
    push    result  ; [i, i, result_addr]
    load            ; [i, i, result]
    add             ; [i, new_result]
    push    result  ; [i, new_result, result_addr]
    save            ; [i]
    push    loop    ; [i, loop_addr]
    jmp             ; [i]

break:
    pop             ; []
    push    result  ; [result_addr]
    load            ; [result]
    push    port    ; [result, port_addr]
    load            ; [result, port]
    out             ; []
    halt
