#!/usr/bin/env python3
from arquibot.rars import Rars

# ─────────────────────────────────────────────────
# ─── TEST 5:
# ─── Una unica palabra en el segmento de datos
# ─────────────────────────────────────────────────

# ── Comenzar la comprobación
Rars("asm/data-1word.s", expected_data=True)

# ── Terminar
Rars.exit()
