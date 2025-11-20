        .data

        #-- Offset 0
        .string "Cadena 0"

        #-- Offset 9
        .string "Cadena x"   #-- Error introducido

        #-- Offset 18
        .string "Cadena Test2"

        .text

        #-- Terminar
        li a7, 10
        ecall
    