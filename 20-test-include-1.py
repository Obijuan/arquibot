#!/usr/bin/env python3
from arquibot.rars import Rars


# ─────────────────────────────────────────────────
# ─── TEST 20
# ─────────────────────────────────────────────────

# -- Preparar el contexto
test = Rars(
            "asm/test-include1.s",  # -- Main
            "asm/servicios.s",  # -- Include
       )

# -- Terminar
test.exit()
