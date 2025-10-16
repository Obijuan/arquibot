#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
#    MAIN
# ───────────────────────────────────────

# -- Valores esperados para las variables
data_ok = {
    "a": 10,
    "b": 20,
    "f": 36
}

# -- Preparar el contexto
Rars("asm/2025-10-10-P1-AC-Teleco-calculo-sol.s",
     expected_data=True,
     bonus=10)

Rars.check_variables(data_ok)

# -- Terminar
Rars.exit()
