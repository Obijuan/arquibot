#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
#    MAIN
# ───────────────────────────────────────

# ── Comenzar la comprobación
print("═════════════ TEST 1 ════════════════════════")
test1 = Rars("asm/wrong-file.s")

print("═════════════ TEST 2 ════════════════════════")
test2 = Rars("asm/test-blank.s")

print("═════════════ TEST 3 ════════════════════════")
test3 = Rars("asm/test-blank-data.s", expected_data=True)

print("═════════════ TEST 4 ════════════════════════")
test4 = Rars("asm/test-blank-text.s")

print("═════════════ TEST 5 ════════════════════════")
test5 = Rars("asm/test-data-1word.s", expected_data=True)

print("═════════════ TEST 6 ════════════════════════")
test6 = Rars("asm/test-data-syntax-error.s", expected_data=True)

print("═════════════ TEST 7 ════════════════════════")
test7 = Rars("asm/test-data-syntax-error2.s", expected_data=True)

print("═════════════ TEST 8 ════════════════════════")
test8 = Rars("asm/test-data-syntax-error3.s", expected_data=True)

print("═════════════ TEST 9 ════════════════════════")
test9 = Rars("asm/test-text-1inst.s", expected_data=True)
test9.exit()

print("═════════════ TEST 10 ════════════════════════")
test10 = Rars("asm/test-text-exit.s", expected_data=True)
test10.exit()

print("═════════════ TEST 11 ════════════════════════")
test11 = Rars("asm/test-text-syntax-error.s", expected_data=True)
test11.exit()

print("═════════════ TEST 12 ════════════════════════")
test12 = Rars("asm/test-variables.s", expected_data=True)

# ── Valores esperados para las variables
data_ok = {
    "a": 1,
    "b": 2,
    "f": 3
}
# ── Comprobar los valores de las variables
test12.check_variables(data_ok)
test12.exit()

print("═════════════ TEST 13 ════════════════════════")
# ── Comenzar la comprobación
test13 = Rars("asm/test-consola-out1.s", expected_data=True)

# ── Mostrar la salida generada por el programa
test13.show_console_output()

# ── Terminar
test13.exit()

print("═════════════ TEST 14 ════════════════════════")
# ── Comenzar la comprobación
test14 = Rars("asm/test-consola-out1.s", expected_data=True)

# ── Salida esperada para la consola
# ── Es la salida correcta
salidas_esperadas = [
    "Test..."
]

# ── Comprobar la salida de la consola
test14.check_console_output(salidas_esperadas)

# ── Terminar
test14.exit()


print("═════════════ TEST 15 ════════════════════════")
# ── Comenzar la comprobación
test15 = Rars("asm/test-consola-out1.s", expected_data=True)

# ── Salida esperada para la consola
# ── Es una salida INCORRECTA
salidas_esperadas = [
    "Test...."
]

# ── Comprobar la salida de la consola
test15.check_console_output(salidas_esperadas)

# ── Terminar
test15.exit()

print("═════════════ TEST 16 ════════════════════════")
test16 = Rars("asm/test-consola-out2.s", expected_data=True)

salidas_esperadas = [
    "Test...",
    "Test...\n"
]

# ── Comprobar la salida de la consola
test16.check_console_output(salidas_esperadas)

# ── Terminar
test16.exit()
