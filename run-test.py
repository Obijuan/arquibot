#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
#    MAIN
# ───────────────────────────────────────


def check_string(offset, var, cadena_esperada):

    # -- Leer la cadena
    cad = Rars.load_string(offset)

    # -- Comprobar si es la cadena esperada
    if cad == cadena_esperada:
        print(f"> ✅️ {var}: {cadena_esperada} ")
    else:
        print(f"> ❌️ {var}: {cad}\n"
              f"     Debería ser: {cadena_esperada}")
        Rars.errors = True


# -- Valores esperados para la salida en consola
SALIDA_ESPERADA = [
    "Introduce cadena de prueba: Cadena copiada y convertida: HOLA",
    "Introduce cadena de prueba: \nCadena copiada y convertida: HOLA",
]

CAD_ORIGEN_ESPERADA = "hola\n"
CAD_DESTINO_ESPERADA = "HOLA"

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
check_string(0, "Destino", CAD_DESTINO_ESPERADA)

# -- Cadena origen
check_string(10, "Origen", CAD_ORIGEN_ESPERADA)

# -- Comprobar la salida del programa
Rars.check_console_output(SALIDA_ESPERADA)


# -- Terminar
Rars.exit()
