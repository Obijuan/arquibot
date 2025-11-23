#!/usr/bin/env python3
from arquibot.rars import Rars


# -- Preparar el contexto
test = Rars(
      "asm/sep.s",    # -- Main
      "asm/system.s",           # -- Include
      expected_data=True,   # -- Segmento de datos
      input="test*\n",  # -- Entrada estandar
      tipo_bonus=Rars.BONUS_CICLOS,
      bonus=64
    )

# -- Valores esperados para las cadenas
CAD_ORIGEN_ESPERADA = "test*\n"

# -- Valores esperados para la salida en consola
SALIDA_ESPERADA = [
    "Escribe una palabra: Caracteres: t-e-s-t-*\nd",
]

Rars.print_section("Comprobando cadenas")

# -- Comprobar Cadena origen
test.check_string(0, CAD_ORIGEN_ESPERADA, var_name="Origen")

# -- Comprobar la salida del programa
test.check_console_output(SALIDA_ESPERADA)


# -- Terminar
test.exit()
