#!/usr/bin/env python3
from arquibot.rars import Rars


# ─────────────────────────────────────────────────
# ─── TEST 22
# ─────────────────────────────────────────────────

Rars(
      "asm/test-input1.s",  # -- Main
      "asm/servicios.s",    # -- Include

      # -- Simular texto introducido por el usuario
      input="Test"
    )

# -- Comprobar si el texto introducido esta en la memoria
Rars.check_string(0, "Test\n", var_name="cad")

# -- Terminar
Rars.exit()
