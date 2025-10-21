#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
#    MAIN
# ───────────────────────────────────────

# -- Valores esperados para las variables
data_ok = {
    "var0": 0xCAFEBACA,
    "a": 10,
    "b": 100,
    "f": 57
}

# -- Preparar el contexto
Rars("asm/term.s",
     expected_data=True,
     bonus=11)

Rars.check_variables(data_ok)

# -- Terminar
Rars.exit()
