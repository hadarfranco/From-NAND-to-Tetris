@R13
D=M
@divisor
M=D

@result
M=0

@divisor
D=M
@R14
D=D-M
@END1
D,JLT
(LOOP1)
    @mul
    M=1
    @counter
    M=0
    @R14
    D=M
    @tempb
    M=D
    (LOOP2)
        @mul
        M=M<<
        @counter
        D=M+1
        M=D
        @tempb
        M=M<<
        D=M
        @divisor
        D=D-M
        @LOOP2
        D,JLE              
    (END2)
    @temp1
    M=1
    @counter
    D=M-1
    M=D
    @END3
    D,JEQ
    (LOOP3)
        @temp1
        M=M<<
        @counter
        D=M-1
        M=D
        @LOOP3
        D,JGT
    (END3)
    @temp1
    D=M
    @result
    D=D+M
    M=D
    @tempb
    M=M>>
    D=M
    @divisor
    D=M-D
    M=D
    @R14
    D=D-M
    @LOOP1
    D,JGE
(END1)
@result
D=M
@R15
M=D



