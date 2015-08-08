@R1
D=M
@R2
M=0
@i
M=D
@END
D,JEQ
(LOOP)
    @R2
    D=M
    @R0
    D=D+M //D=value of R0+value of R0
    @R2
    M=D
    @i
    D=M
    D=D-1
    M=D   
    @END    
    D;JLE // If D=0 goto END
    @LOOP  
    0;JMP // jump to loop
(END)
