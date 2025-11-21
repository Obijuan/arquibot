#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
#    MAIN
# ───────────────────────────────────────

# ── Comenzar la comprobación
test1 = Rars("asm/wrong-file.s")
test2 = Rars("asm/test-blank.s")
test3 = Rars("asm/test-blank-data.s", expected_data=True)
test4 = Rars("asm/test-blank-text.s")
test5 = Rars("asm/test-data-1word.s", expected_data=True)
