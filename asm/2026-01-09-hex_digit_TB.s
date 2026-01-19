#---------------------------------------------------
#-- Programa de prueba de la funcion hex_digit()
#---------------------------------------------------
#-- Se hacen las siguientes llamadas para comprobar la función
#-- hex_digit(5) = '5'
#-- hex_digit(10) = 'A'
#-- hex_digit(15) = 'F'

	.globl main

    # -- Servicios del sistema operativo
    .include "so.h"

    # -- Funciones para realizar los tests
    .include "test.h"
	

#------------------------------
# -- Comprobar 
.macro CHECK_FUNCTION1(%val1)

    #-- Dar valores a TODOs los registros temporales y de argumento
    #-- para asegurar que la funcion llamada no asume que tienen
    #-- el valor 0
    init_temp_regs

    #-- Dar valores conocidos a los registros estaticos
    #-- Estos valores debe PERMANECER INALTERADOS
    #-- tras llamar a la funcion
    init_static_regs

    #-- Llamar a la funcion con el valor pasado
    li a0, %val1
    jal hex_digit

    #-- Imprimir el resultado en la consola
    PRINT_CHARR(a0)
    PRINT_CHARI('\n')

	#-- Comprobar que los registros estaticos no se han
    #-- modificado
    check_static_regs

.end_macro

.macro ASSERT(%val_exp)
    li t0, %val_exp
    beq a0, t0, test_ok

    #-- NO pasa el test
    mv t1, a0
    PRINT_STRINGI("ERROR. Valor: ")
    mv a0, t1
    PRINT_INT_HEXR(a0)
    PRINT_STRINGI(" != ")
    PRINT_INT_HEXR(t0)
    PRINT_CHARI('\n')
    j next

    #-- Pasa el test
 test_ok:
    PRINT_STRINGI("OK\n")

 next:

.end_macro

	.text

main:
	
    #----------- Test 1: Comprobar hex_digit(5)
    PRINT_STRINGI("* hex_digit(5): ")
    init_temp_regs
    init_static_regs

    li a0, 5
    jal hex_digit

    ASSERT('5')
    check_static_regs
    #PRINT_CHARI('\n')

    #----------- Test 2: Comprobar hex_digit(10)
    PRINT_STRINGI("* hex_digit(10): ")
    init_temp_regs
    init_static_regs

    li a0, 10
    jal hex_digit

    ASSERT('A')
    check_static_regs
    #PRINT_CHARI('\n')


	#-- Terminar
	EXIT
	
	