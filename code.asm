port:
    WORD    1
loop:
    PUSH    break
    PUSH    port
    IN
    JZ
    PUSH    break
    SWAP
    PUSH    port
    OUT
    PUSH    loop
    JMP
break:
    HALT
