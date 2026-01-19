#---------------------------------------------------
#-- Programa de prueba de la funcion print_hex1()
#---------------------------------------------------
#-- Se hacen las siguientes llamadas para comprobar la función
#-- print_hex1(5) = '0x5'
#-- print_hex1(10) = '0xA'
#-- print_hex1(15) = '0xF'

	.globl main

    # -- Servicios del sistema operativo
    .include "so.h"

    # -- Funciones para realizar los tests
    .include "test.h"
	

	.text

main:
	
    #----------- Test 1: Comprobar print_hex1(5)
    init_temp_regs
    init_static_regs

    li a0, 5
    jal print_hex1
    PRINT_CHARI('\n')

    check_static_regs

    #----------- Test 1: Comprobar print_hex1(10)
    init_temp_regs
    init_static_regs

    li a0, 10
    jal print_hex1
    PRINT_CHARI('\n')

    check_static_regs
    


	#-- Terminar
	EXIT
	
	