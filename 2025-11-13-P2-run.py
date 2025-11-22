#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
#    MAIN
# ───────────────────────────────────────

# -- Preparar el contexto
test = Rars(
      "asm/2025-11-13-P2-AC-Teleco-copyupper.s",    # -- Main
      "asm/so.s",           # -- Include
      expected_data=True,   # -- Segmento de datos
      input="hola\n",  # -- Entrada estandar
      tipo_bonus=Rars.BONUS_CICLOS,
      bonus=59
    )

# -- Valores esperados para las cadenas
CAD_ORIGEN_ESPERADA = "hola\n"
CAD_DESTINO_ESPERADA = "HOLA"

# -- Valores esperados para la salida en consola
SALIDA_ESPERADA = [
    "Introduce cadena de prueba: Cadena copiada y convertida: HOLA",
    "Introduce cadena de prueba: \nCadena copiada y convertida: HOLA",
    "Introduce cadena de prueba:Cadena copiada y convertida:HOLA",
    "Introduce cadena de prueba: \nCadena copiada y convertida:HOLA",
    "Introduce una cadena de prueba: Cadena copiada y convertida: HOLA",
    "Introduce una cadena de prueba:\nCadena copiada y convertida:HOLA",
    "Introduce la cadena de prueba: Cadena copiada y convertida: HOLA",
]

Rars.print_section("Comprobando cadenas")

# -- Comprobar cadena destino
test.check_string(0, CAD_DESTINO_ESPERADA, var_name="Destino")

# -- Comprobar Cadena origen
test.check_string(10, CAD_ORIGEN_ESPERADA, var_name="Origen")

# -- Comprobar la salida del programa
test.check_console_output(SALIDA_ESPERADA)


# -- Terminar
test.exit()
