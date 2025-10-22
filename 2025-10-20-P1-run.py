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
    "c": 57
}

# -- Preparar el contexto
Rars("asm/2025-10-20-P1-ASA-II-term.s",
     expected_data=True,
     bonus=11)

Rars.check_variables(data_ok)

# -- Comprobar que se ha usado el registro x9
reg_x9_ok = Rars.regs[9] == 57
if reg_x9_ok:
    print(f"> ✅️ Registro x9: {Rars.regs[9]}")
else:
    Rars.print_error("Valor incorrecto en registro x9")

# -- Terminar
Rars.exit()
