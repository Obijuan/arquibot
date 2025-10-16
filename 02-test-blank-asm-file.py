#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
# ─── TEST 2: Fichero asm en blanco
# ─── No hay segmento de codigo
# ─── No hay segmento de datos
# ───────────────────────────────────────

# ── Comenzar la comprobación
Rars("asm/blank.s", expected_data=True)

# ── Terminar
Rars.exit()
