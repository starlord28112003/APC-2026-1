```asm
INP
STA A

INP
STA B

LDA ZERO
STA RES

LOOP   LDA B
       BRZ FIM

       SUB ONE
       STA B

       LDA RES
       ADD A
       STA RES

       BRA LOOP

FIM    LDA RES
       OUT
       HLT

A      DAT 0
B      DAT 0
RES    DAT 0
ONE    DAT 1
ZERO   DAT 0
```

