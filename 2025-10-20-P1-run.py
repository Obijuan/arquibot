#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
#    MAIN
# ───────────────────────────────────────


# -- Preparar el contexto
test = Rars("asm/2025-10-20-P1-ASA-II-term.s",
            expected_data=True,
            bonus=11)

# -- Valores esperados para las variables
data_ok = {
    "var0": 0xCAFEBACA,
    "a": 10,
    "b": 100,
    "c": 57
}

test.check_variables(data_ok)

# -- Comprobar que se ha usado el registro x9
reg_x9_ok = test.regs[9] == 57
if reg_x9_ok:
    print(f"> ✅️ Registro x9: {test.regs[9]}")
else:
    test.print_error("Valor incorrecto en registro x9")

# -- Terminar
test.exit()
