@24576
D=A
@keyboard //0 if not pressed else 1
M=D

@16384
D=A
@screenstart
M=D
@pointer
M=D

@24575
D=A
@screenend
M=D

(KEYBOARD)
    @keyboard
    A=M
    D=M
    @UNFILL
    D,JEQ
    @FILL
    D,JNE
(ENDKEYBOARD)

(FILL)
    @pointer
    A=M
    M=-1
    @pointer
    D=M
    @screenend
    D=D-M
    @KEYBOARD
    D,JEQ
    @pointer
    D=M+1
    M=D
    @KEYBOARD
    0,JMP
(ENDFILL)

(UNFILL)
    @pointer
    A=M
    M=0
    @pointer
    D=M
    @screenstart
    D=D-M
    @KEYBOARD
    D,JEQ
    @pointer
    D=M-1
    M=D
    @KEYBOARD
    0,JMP
(ENDUNFILL)



