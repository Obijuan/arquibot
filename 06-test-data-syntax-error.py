#!/usr/bin/env python3
from arquibot.rars import Rars

# ─────────────────────────────────────────────────
# ─── TEST 6:
# ─── Solo hay segmento de datos
# ─── con Error sintactico
# ─────────────────────────────────────────────────

# ── Comenzar la comprobación
Rars("asm/data-syntax-error.s", expected_data=True)
