port:
    WORD    1
loop:
    PUSH    break
    PUSH    port
    LOAD
    IN
    JZ
    PUSH    break
    SWAP
    PUSH    port
    LOAD
    OUT
    PUSH    loop
    JMP
break:
    HALT
