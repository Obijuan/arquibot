#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
#    MAIN
# ───────────────────────────────────────

# ── Comenzar la comprobación
test1 = Rars("asm/wrong-file.s")
test2 = Rars("asm/test-blank.s")
test3 = Rars("asm/test-blank-data.s", expected_data=True)

# ── Terminar
# Rars.exit()
