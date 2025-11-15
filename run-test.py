#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
#    MAIN
# ───────────────────────────────────────

# -- Valores esperados para la salida en consola
SALIDA_ESPERADA = [
    "Introduce cadena de prueba: Cadena copiada y convertida: HOLA",
    ""
]

# -- Preparar el contexto
Rars(
      "asm/copyupper.s",    # -- Main
      "asm/so.s",           # -- Include
      expected_data=True,   # -- Segmento de datos
      input="hola\n",  # -- Entrada estandar
      tipo_bonus=Rars.BONUS_CICLOS,
      bonus=59
    )

# -- Comprobar la salida del programa
Rars.check_console_output(SALIDA_ESPERADA)

# -- Terminar
Rars.exit()
