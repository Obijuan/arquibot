#!/usr/bin/env python3
from arquibot.rars import Rars


# ─────────────────────────────────────────────────
# ─── TEST 18
# ─────────────────────────────────────────────────

# -- Valores esperados para las cadena
CAD0_ESPERADA = "Cadena 0"
CAD1_ESPERADA = "Cadena 1"


# -- Preparar el contexto
test = Rars(
          "asm/test-string2.s",  # -- Main
          expected_data=True,    # -- Segmento de datos
      )

Rars.print_section("Comprobando cadenas")

# -- Comprobar cadenas
# -- Se pasa el offset y el valor esperado
test.check_string(0, CAD0_ESPERADA, var_name="Cad0")
test.check_string(9, CAD1_ESPERADA, var_name="Cad1")

# -- Terminar
test.exit()
