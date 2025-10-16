#!/usr/bin/env python3
from arquibot.rars import Rars

# ─────────────────────────────────────────────────
# ─── TEST 9:
# ─────────────────────────────────────────────────

# ── Comenzar la comprobación
Rars("asm/text-1inst.s", expected_data=True)

# ── Terminar
Rars.exit()
