#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
#    MAIN
# ───────────────────────────────────────

# -- Valores esperados para las cadenas
CAD_ORIGEN_ESPERADA = "hola\n"
CAD_DESTINO_ESPERADA = "HOLA"

# -- Valores esperados para la salida en consola
SALIDA_ESPERADA = [
    "Introduce cadena de prueba: Cadena copiada y convertida: HOLA",
    "Introduce cadena de prueba: \nCadena copiada y convertida: HOLA",
    "Introduce cadena de prueba:Cadena copiada y convertida:HOLA"
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

Rars.print_section("Comprobando cadenas")

# -- Comprobar cadena destino
Rars.check_string(0, CAD_DESTINO_ESPERADA, var_name="Destino")

# -- Comprobar Cadena origen
Rars.check_string(10, CAD_ORIGEN_ESPERADA, var_name="Origen")

# -- Comprobar la salida del programa
Rars.check_console_output(SALIDA_ESPERADA)


# -- Terminar
Rars.exit()
