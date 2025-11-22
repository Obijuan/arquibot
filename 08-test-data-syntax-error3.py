#!/usr/bin/env python3
from arquibot.rars import Rars

# ─────────────────────────────────────────────────
# ─── TEST 7:
# ─── Solo hay segmento de datos
# ─── con Error sintactico
# ─────────────────────────────────────────────────

# ── Comenzar la comprobación
Rars("asm/test-data-syntax-error3.s", expected_data=True)
