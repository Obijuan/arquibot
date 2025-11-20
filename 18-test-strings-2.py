#!/usr/bin/env python3
from arquibot.rars import Rars


# ─────────────────────────────────────────────────
# ─── TEST 18
# ─────────────────────────────────────────────────

# -- Valor esperado para la cadena
CAD0_ESPERADA = "Cadena 0"
CAD1_ESPERADA = "Cadena 1"


# -- Preparar el contexto
Rars(
      "asm/test-string2.s",  # -- Main
      expected_data=True,    # -- Segmento de datos
    )

Rars.print_section("Comprobando cadenas")

# -- Comprobar cadenas
# -- Se pasa el offset y el valor esperado
Rars.check_string(0, CAD0_ESPERADA, var_name="Cad0")
Rars.check_string(9, CAD1_ESPERADA, var_name="Cad1")

# -- Terminar
Rars.exit()
