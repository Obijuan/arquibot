#!/usr/bin/env python3
from arquibot.rars import Rars

# ─────────────────────────────────────────────────
# ─── TEST 10:
# ─────────────────────────────────────────────────

# ── Comenzar la comprobación
test = Rars("asm/test-text-exit.s", expected_data=True)

# ── Terminar
test.exit()
