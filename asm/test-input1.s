
    .include "servicios.s"

    .eqv MAX 20

        .data

        #-- Offset 0
cad:    .space MAX

    .text

    #-- Pedir cadena al usuario
    la a0, cad
    li a1, MAX
    li a7, READ_STRING
    ecall

    #-- Terminar
    li a7, EXIT
    ecall