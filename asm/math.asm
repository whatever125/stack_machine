; math

section data:
    a:      3
    b:      -5
    c:      2

section code:       ; (a + b) * c
    start:
        push    c
        load
        push    b
        load
        push    a
        load
        add
        mul
    break:
        halt
