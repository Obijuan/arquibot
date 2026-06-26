#---------------------------------------------------
#-- Programa de prueba de la funcion polinomio
#---------------------------------------------------
#-- Se hacen las siguientes llamadas para comprobar la función
#-- polinomio(1) = 3
#-- polinomio(2) = 7
#-- polinomio(5) = 31

	.globl main

    # -- Servicios del sistema operativo
    .include "so.h"

    # -- Funciones para realizar los tests
    .include "test.h"

    .data
cad: .space 10

#-- Resultados esperados
    .eqv r1, 3
    .eqv r2, 7
    .eqv r3, 31

    .text
#------------------------------

.macro ASSERT_EQ(%reg, %value)

    #-- Guardar registro s0 y s1 en la pila
    addi sp, sp, -16
    sw s0, 0(sp)
    sw s1, 4(sp)

    #-- Comparar si reg = value
    li a1, %value
    mv a0, %reg
    bne a0, a1, test_fail1

    #-- Pasa el test
    PRINT_STRINGI("OK\n")
    j next

 test_fail1:
    #-- NO pasa el test
    PRINT_STRINGI("ERROR\n")
    PRINT_STRINGI("  * Obtenida: ")
    PRINT_INTR(s0)
    PRINT_CHARI('\n')
    PRINT_STRINGI("  * Esperada: ")
    PRINT_INTR(s1)
    PRINT_CHARI('\n')

  next:

    #-- Recuperar registros s0 y s1
    lw s0, 0(sp)
    lw s1, 4(sp)
    addi sp, sp, 16

.end_macro

	.text

main:

    #----------- Test 1: Comprobar polinomio(1)
    PRINT_STRINGI("* polinomio(1): ")
    init_temp_regs
    init_static_regs

    #-- Llamar a polinomio(1)
    li a0, 1
    jal polinomio

    #-- Comprobar resultado
    ASSERT_EQ(a0, r1)

    #----------- Test 2: Comprobar polinomio(2)
    PRINT_STRINGI("* polinomio(2): ")
    init_temp_regs
    init_static_regs

    #-- Llamar a polinomio()
    li a0, 2
    jal polinomio

    #-- Comprobar resultado
    ASSERT_EQ(a0, r2)

    #----------- Test 3: Comprobar polinomio(5)
    PRINT_STRINGI("* polinomio(5): ")
    init_temp_regs
    init_static_regs

    #-- Llamar a polinomio()
    li a0, 5
    jal polinomio

    #-- Comprobar resultado
    ASSERT_EQ(a0, r3)

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

