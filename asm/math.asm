section data:
    a:      3
    b:      -5
    c:      2

section code:       ; (a + b) * c
    start:
        PUSH    c
        LOAD
        PUSH    b
        LOAD
        PUSH    a
        LOAD
        ADD
        MUL
    break:
        HALT
