#!/usr/bin/env python3
from arquibot.rars import Rars

# ─────────────────────────────────────────────────
# ─── TEST 9:
# ─────────────────────────────────────────────────

# ── Comenzar la comprobación
test = Rars("asm/test-text-1inst.s", expected_data=True)
test.exit()
