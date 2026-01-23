#!/usr/bin/env python3
from arquibot.rars import Rars


SALIDA_ESPERADA = ["""\
0x0
0x1
0x2
0x3
0x4
0x5
0x6
0x7
0x8
0x9
0xA
0xB
0xC
0xD
0xE
0xF
"""]


# -- Ejecutar programa asm
test = Rars(
      "asm/2026-01-09-main.s",      # -- Main
      deps=["asm/2026-01-09-hex_digit_SOL.s",
            "asm/2026-01-09-print_hex1_SOL.s"],  # -- Dependencias
    )

# -- Mostrar la salida en consola
test.show_console_output()

# -- Comprobar la salida del programa
ok = test.check_console_output(SALIDA_ESPERADA)

# -- Test finales
test.exit()
