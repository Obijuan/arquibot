#---------------------------------------------------
#-- Programa de prueba de la funcion print_bin()
#---------------------------------------------------
#-- Se hacen las siguientes llamadas para comprobar la función
#-- print_bin(255) = '0b11111111'
#-- print_bin(2) = '0b00000010'

	.globl main

    # -- Servicios del sistema operativo
    .include "so.h"

    # -- Funciones para realizar los tests
    .include "test.h"
	

	.text

main:
	
    #----------- Test 1: Comprobar print_bin(255)
    init_temp_regs
    init_static_regs

    li a0, 255
    jal print_bin
    PRINT_CHARI('\n')

    check_static_regs

    #----------- Test 2: Comprobar print_bin(2)
    init_temp_regs
    init_static_regs

    li a0, 2
    jal print_bin
    PRINT_CHARI('\n')

    check_static_regs
    

	#-- Terminar
	EXIT
	
	