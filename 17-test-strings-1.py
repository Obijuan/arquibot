#!/usr/bin/env python3
from arquibot.rars import Rars


# ─────────────────────────────────────────────────
# ─── TEST 17
# ─────────────────────────────────────────────────

# -- Valor esperado para la cadena
CAD0_ESPERADA = "Test..."


# -- Preparar el contexto
Rars(
      "asm/test-string1.s",  # -- Main
      expected_data=True,    # -- Segmento de datos
    )

Rars.print_section("Comprobando cadenas")

# -- Comprobar cadena destino
Rars.check_string(0, CAD0_ESPERADA, var_name="Cadena 0")

# -- Terminar
Rars.exit()
