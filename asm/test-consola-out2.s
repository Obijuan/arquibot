        .data
msg:    .string "Test...\n"

        .text

        #-- Imprimir mensaje en consola
        la a0, msg
        li a7, 4  #-- PRINT_STRING
        ecall

        #-- Terminar
        li a7, 10
        ecall