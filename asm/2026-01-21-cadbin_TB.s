#---------------------------------------------------
#-- Programa de prueba de la funcion cadbin()
#---------------------------------------------------
#-- Se hacen las siguientes llamadas para comprobar la función
#-- cadbin(cad,255) = '11111111'
#-- cadbin(cad,2) = '00000010'

	.globl main

    # -- Servicios del sistema operativo
    .include "so.h"

    # -- Funciones para realizar los tests
    .include "test.h"
	
    .data
cad: .space 10

#-- Resultados esperados
r1:  .string "11111111"
r2:  .string "00000010"

    .text
#------------------------------

.macro ASSERT_EQ_STR(%cad1, %cad2)
    #-- Comparar si la cadena obtenida es igual a la esperada
    la a0, %cad1
    la a1, %cad2
    jal cmpstr

    beq a0, zero, test_fail1

    #-- Pasa el test
    PRINT_STRINGI("OK\n")
    j next

 test_fail1:
    #-- NO pasa el test
    PRINT_STRINGI("ERROR\n")
    PRINT_STRINGI("  * Obtenida: ")
    PRINT_STRINGL(%cad1)
    PRINT_CHARI('\n')
    PRINT_STRINGI("  * Esperada: ")
    PRINT_STRINGL(%cad2)
    PRINT_CHARI('\n')

  next:
 
.end_macro

	.text

main:
	
    #----------- Test 1: Comprobar cadbin(cad, 255)
    PRINT_STRINGI("* cadbin(cad, 255): ")
    init_temp_regs
    init_static_regs

    #-- Llamar a cadbin()
    la a0, cad
    li a1, 255
    jal cadbin

    #-- Comprobar resultado
    ASSERT_EQ_STR(cad, r1)

    #-- Comprobar que los registros estáticos NO se han modificado
    check_static_regs

    #----------- Test 2: Comprobar cadbin(cad, 2)
    PRINT_STRINGI("* cadbin(cad, 2): ")
    init_temp_regs
    init_static_regs

    #-- Llamar a cadbin()
    la a0, cad
    li a1, 2
    jal cadbin

    #-- Comprobar resultado
    ASSERT_EQ_STR(cad, r2)

    #-- Comprobar que los registros estáticos NO se han modificado
    check_static_regs

	#-- Terminar
	EXIT
	
	

#--------------------------------------------
#-- cmpstr(str1, str2)
#--
#-- Comparar dos cadenas
#--
#-- ENTRADA:
#--   - a0 (str1): Puntero a cadena 1
#--   - a1 (str2): Puntero a cadena 2
#--
#-- SALIDA:
#--   - a0: Resultado de la comparacion
#--     - 0: NO son iguales
#--     - 1: Son iguales
#---------------------------------------------
cmpstr:

 cmpstr_next:
	#-- Leer caracteres fuente y destino
	lb t0, 0(a0)
	lb t1, 0(a1)

	#-- Compararlos!
	bne t0, t1, cmpstr_not_equal

	#-- Los caracteres son iguales
	#-- comprobar si hemos llegado al final de la 
	#-- cadena destino
	beq t1, zero, cmpstr_end_equal

	#--- No se ha llegado al final
	#--- Incrementar punteros de las cadenas origen y destino
	addi a0, a0, 1
	addi a1, a1, 1

	#-- Siguiente caracter
	j cmpstr_next

 cmpstr_not_equal: 
    #-- Las cadenas NO son iguales
	li a0, 0
	j cmpstr_end

 cmpstr_end_equal:
	#-- Las cadenas son iguales!!
	li a0, 1

 cmpstr_end:
	ret

