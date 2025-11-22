#!/usr/bin/env python3
from arquibot.rars import Rars


# ─────────────────────────────────────────────────
# ─── TEST 19
# ─────────────────────────────────────────────────

# -- Preparar el contexto
test = Rars(
         "asm/test-string3.s",  # -- Main
         expected_data=True,    # -- Segmento de datos
       )

Rars.print_section("Comprobando cadenas")

# -- Valores esperados para las cadena
CAD0_ESPERADA = "Cadena 0"
CAD1_ESPERADA = "Cadena 1"
CAD2_ESPERADA = "Cadena Test2"

# -- Comprobar cadenas
# -- Se pasa el offset y el valor esperado
test.check_string(0, CAD0_ESPERADA, var_name="Cad0")
test.check_string(9, CAD1_ESPERADA, var_name="Cad1")
test.check_string(18, CAD2_ESPERADA, var_name="Cad2")

# -- Terminar
test.exit()
