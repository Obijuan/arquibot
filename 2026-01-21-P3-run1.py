#!/usr/bin/env python3
from arquibot.rars import Rars

# -- Salida esperada:
# * cadbin(cad, 255): OK
# * Convenio: OK
# * cadbin(cad, 2): OK
# * Convenio: OK


# -- Ejecutar programa asm
test = Rars(
      "asm/2026-01-21-cadbin_TB.s",      # -- Main
      deps=["asm/2026-01-21-cadbin.s"],  # -- Dependencias
    )

# -- Mostrar la salida en consola
test.show_console_output()

# -- Comprobar el resultado de la ejecucion del testbench
test.print_section("Resultado")

if "cadbin(cad, 255): OK" in test.stdout:
    print("> ✅️ Test 1 OK")
else:
    test.print_error("Test 1 incorrecto")

if "cadbin(cad, 2): OK" in test.stdout:
    print("> ✅️ Test 2 OK")
else:
    test.print_error("Test 2 incorrecto")

if "Convenio: OK" in test.stdout:
    print("> ✅️ Test convenio OK")

if "ERROR" in test.stdout:
    test.print_error("Funcionalidad incorrecta")

if "NO CUMPLE!!" in test.stdout:
    test.print_error("Violacion del convenio de registros")

# -- Comprobar si se superan los ciclos máximo
# -- Si es asi, significa que hay un bucle infinito
if test.ciclos >= Rars.MAX_STEPS:
    test.print_error("BUCLE INFINITO")

test.close_line()
