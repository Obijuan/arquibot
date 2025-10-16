#!/usr/bin/env python3
from arquibot.rars import Rars

# ─────────────────────────────────────────────────
# ─── TEST 12
# ─────────────────────────────────────────────────

# ── Valores esperados para las variables
data_ok = {
    "a": 1,
    "b": 2,
    "f": 3
}

# ── Comenzar la comprobación
Rars("asm/variables.s", expected_data=True)

# ── Comprobar los valores de las variables
Rars.check_variables(data_ok)

# ── Terminar
Rars.exit()
