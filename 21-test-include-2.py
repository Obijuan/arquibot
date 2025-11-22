#!/usr/bin/env python3
from arquibot.rars import Rars


# ─────────────────────────────────────────────────
# ─── TEST 21
# ─────────────────────────────────────────────────

# -- Se especifica un fichero include QUE NO EXISTE!
test = Rars(
          "asm/test-include1.s",    # -- Main
          "asm/servicios-error.s",  # -- Include
       )

# -- Terminar
test.exit()
