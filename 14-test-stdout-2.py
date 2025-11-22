#!/usr/bin/env python3
from arquibot.rars import Rars

# ─────────────────────────────────────────────────
# ─── TEST 14
# ─────────────────────────────────────────────────

# ── Salida esperada para la consola
# ── Es la salida correcta
salidas_esperadas = [
    "Test..."
]

# ── Comenzar la comprobación
test = Rars("asm/test-consola-out1.s", expected_data=True)

# ── Comprobar la salida de la consola
test.check_console_output(salidas_esperadas)

# ── Terminar
test.exit()
