#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
# ─── TEST 1: Fichero asm incorrecto
# ───────────────────────────────────────

# ── Comenzar la comprobación
Rars("asm/wrong-file.s")

# ── Terminar
Rars.exit()
