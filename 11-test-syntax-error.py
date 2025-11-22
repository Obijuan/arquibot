#!/usr/bin/env python3
from arquibot.rars import Rars

# ─────────────────────────────────────────────────
# ─── TEST 11:
# ─────────────────────────────────────────────────

# ── Comenzar la comprobación
test = Rars("asm/test-text-syntax-error.s", expected_data=True)

# ── Terminar
test.exit()
