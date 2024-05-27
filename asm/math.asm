a:
    WORD    3
b:
    WORD    -1
c:
    WORD    2
offset:
    WORD    48
port:
    WORD    1
start:
    PUSH    offset
    LOAD
    PUSH    c
    LOAD
    PUSH    b
    LOAD
    PUSH    a
    LOAD
    ADD
    MUL
    ADD
    PUSH    port
    LOAD
    OUT
break:
    HALT
