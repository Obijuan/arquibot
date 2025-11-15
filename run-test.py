#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
#    MAIN
# ───────────────────────────────────────

# -- Valores esperados para la salida en consola
SALIDA_ESPERADA = [
    "Introduce cadena:Cadena sin espacios finales:TESTTEST*",
    "otra opcion"
]

# -- Preparar el contexto
Rars(
      "asm/spacefin.s",     # -- Main
      "asm/ecall.s",        # -- Include
      expected_data=True,   # -- Segmento de datos
      input="TEST     \n",  # -- Entrada estandar
      tipo_bonus=Rars.BONUS_CICLOS,
      bonus=49
    )

# -- Comprobar la salida del programa
Rars.check_console_output(SALIDA_ESPERADA)

# -- Terminar
Rars.exit()
