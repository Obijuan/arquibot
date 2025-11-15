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
Rars("asm/consola-out1.s", expected_data=True)

# ── Comprobar la salida de la consola
Rars.check_console_output(salidas_esperadas)

# ── Terminar
Rars.exit()
