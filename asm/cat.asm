section data:
    port:   1
section code:
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