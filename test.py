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
Rars("../calculo.s", bonus=10)

Rars.check_variables(data_ok)

# -- Terminar
Rars.exit()
