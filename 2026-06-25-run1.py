#!/usr/bin/env python3
from arquibot.rars import Rars


def assert_string_in_stdout(test: Rars, cad: str):
    if cad in test.stdout:
        print(f"> ✅️ {cad}")
    else:
        test.print_error(f"{cad}")


# -- Ejecutar programa asm
test = Rars(
      "asm/2026-06-25-main1.s",      # -- Main
      deps=["asm/2026-06-25-mul2u.s"],  # -- Dependencias
      input="2\n3\n8\n4\n-1\n",
      expected_data=True,   # -- Segmento de datos
    )

if test.ok:

    # -- Mostrar la salida en consola
    test.show_console_output()

    # -- Comprobar el resultado de la ejecucion del testbench
    Rars.print_section("Comprobando cadenas")
    assert_string_in_stdout(test, "Introduzca numero a:")
    assert_string_in_stdout(test, "Introduzca numero b:")
    assert_string_in_stdout(test, "2 * 3 = 6")
    assert_string_in_stdout(test, "8 * 4 = 32")

    # -- Terminar
    test.exit()
