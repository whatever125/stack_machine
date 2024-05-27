port:
    WORD    1
loop:
    PUSH    break
    PUSH    port
    LOAD
    IN
    DUP
    PUSH    port
    LOAD
    OUT
    JZ
    PUSH    loop
    JMP
break:
    HALT
