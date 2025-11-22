#!/usr/bin/env python3
from arquibot.rars import Rars

# ─────────────────────────────────────────────────
# ─── TEST 13
# ─────────────────────────────────────────────────

# ── Comenzar la comprobación
test = Rars("asm/test-consola-out1.s", expected_data=True)

# ── Mostrar la salida generada por el programa
test.show_console_output()

# ── Terminar
test.exit()
