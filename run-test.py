#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
#    MAIN
# ───────────────────────────────────────

# -- Valores esperados para las variables
data_ok = {
    "a": 1,
    "b": 2,
    "f": 3
}

# -- Preparar el contexto
Rars("asm/test.s", bonus=10)

Rars.check_variables(data_ok)

# -- Terminar
Rars.exit()
