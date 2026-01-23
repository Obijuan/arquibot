#!/usr/bin/env python3
from arquibot.rars import Rars


SALIDA_ESPERADA = ["""\
0b00000000
0b00000001
0b00000010
0b00000011
0b00000100
0b00000101
0b00000110
0b00000111
0b00001000
0b00001001
0b00001010
0b00001011
0b00001100
0b00001101
0b00001110
0b00001111
"""]


# -- Ejecutar programa asm
test = Rars(
      "asm/2026-01-21-main.s",      # -- Main
      deps=["asm/2026-01-21-print_bin_SOL.s",
            "asm/2026-01-21-cadbin_SOL.s"],  # -- Dependencias
    )

# -- Mostrar la salida en consola
test.show_console_output()

# -- Comprobar la salida del programa
ok = test.check_console_output(SALIDA_ESPERADA)

# -- Test finales
test.exit()
