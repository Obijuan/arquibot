#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
#    MAIN
# ───────────────────────────────────────

# ── Comenzar la comprobación
test1 = Rars("asm/wrong-file.s")
test2 = Rars("asm/test-blank.s")
test3 = Rars("asm/test-blank-data.s", expected_data=True)
test4 = Rars("asm/test-blank-text.s")
test5 = Rars("asm/test-data-1word.s", expected_data=True)
test6 = Rars("asm/test-data-syntax-error.s", expected_data=True)
test7 = Rars("asm/test-data-syntax-error2.s", expected_data=True)
test8 = Rars("asm/test-data-syntax-error3.s", expected_data=True)

test9 = Rars("asm/test-text-1inst.s", expected_data=True)
test9.exit()

test10 = Rars("asm/test-text-exit.s", expected_data=True)
test10.exit()

test11 = Rars("asm/test-text-syntax-error.s", expected_data=True)
test11.exit()

# ────────── TEST 12 ────────────────
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

# ────────── TEST 13 ────────────────
# ── Comenzar la comprobación
test13 = Rars("asm/test-consola-out1.s", expected_data=True)

# ── Mostrar la salida generada por el programa
test13.show_console_output()

# ── Terminar
test13.exit()

# ────────── TEST 14 ────────────────
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
