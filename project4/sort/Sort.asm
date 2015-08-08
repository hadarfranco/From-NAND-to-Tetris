@R14
D=M
@address
M=D

@R15
D=M
D=D-1
@length
M=D

(LOOP1)
    // if length=0 end
    @length
    D=M
    @END
    D,JLE
    @address
    D=M
    @index
    M=D
    (LOOP2)        
        // compare between index and index+1
        @index
        D=M
        A=D
        D=M
        @i
        M=D
        @index
        D=M
        D=D+1
        A=D
        D=M
        @j
        M=D
        @i
        D=D-M
        @SWAP
        // if *j-*i>0 swap
        D,JGT
        (BACK)
        // index = index+1
        @index        
        D=M
        D=D+1
        M=D
        // if index = length out else back to loop2
        @length
        D=D-M
        @address
        D=D-M
        @LOOP2
        D,JLT
        @END2
        D,JEQ
    (END2)
    // length = length-1
    @length
    D=M
    D=D-1
    M=D
    // if length=0 end
    @END
    D,JEQ
    // else back to loop1
    @LOOP1
    D,JGT
(END1)

(SWAP)
    @j
    D=M
    @index
    A=M
    M=D

    D=A
    D=D+1
    @temp
    M=D
    @i  
    D=M
    @temp
    A=M
    M=D
    @BACK
    0,JMP
(ENDSWAP)

(END)
