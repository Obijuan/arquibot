#!/usr/bin/env python3
from arquibot.rars import Rars

# ─────────────────────────────────────────────────
# ─── TEST 15
# ─────────────────────────────────────────────────

# ── Salida esperada para la consola
# ── Es una salida INCORRECTA
salidas_esperadas = [
    "Test...."
]

# ── Comenzar la comprobación
test = Rars("asm/test-consola-out1.s", expected_data=True)

# ── Comprobar la salida de la consola
test.check_console_output(salidas_esperadas)

# ── Terminar
test.exit()
