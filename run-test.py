#!/usr/bin/env python3
from arquibot.rars import Rars


print("═════════════ TEST 22 ════════════════════════")
test = Rars(
         "asm/test-input1.s",  # -- Main
         "asm/servicios.s",    # -- Include

         # -- Simular texto introducido por el usuario
         input="Test"
       )

Rars.print_section("Comprobando variables")

# -- Comprobar si el texto introducido esta en la memoria
test.check_string(0, "Test\n", var_name="cad")

# -- Terminar
test.exit()
