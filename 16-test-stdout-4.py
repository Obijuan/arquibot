#!/usr/bin/env python3
from arquibot.rars import Rars

# ─────────────────────────────────────────────────
# ─── TEST 16
# ─────────────────────────────────────────────────

# ── Salida esperada para la consola
# ── Cualquier de las dos podria ser correcta
salidas_esperadas = [
    "Test...",
    "Test...\n"
]

# ── Comenzar la comprobación
Rars("asm/consola-out2.s", expected_data=True)

# ── Comprobar la salida de la consola
Rars.check_console_output(salidas_esperadas)

# ── Terminar
Rars.exit()
