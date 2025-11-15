#!/usr/bin/env python3
from arquibot.rars import Rars

# ─────────────────────────────────────────────────
# ─── TEST 13
# ─────────────────────────────────────────────────

# ── Comenzar la comprobación
Rars("asm/consola-out1.s", expected_data=True)

# ── Mostrar la salida generada por el programa
Rars.show_console_output()

# ── Terminar
Rars.exit()
