#!/usr/bin/env python3
from arquibot.rars import Rars

# ─────────────────────────────────────────────────
# ─── TEST 9:
# ─────────────────────────────────────────────────

# ── Comenzar la comprobación
test = Rars("asm/text-exit.s", expected_data=True)

# ── Terminar
test.exit()
