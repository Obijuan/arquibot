#!/usr/bin/env python3
from arquibot.rars import Rars


def assert_string_in_stdout(test: Rars, cad: str):
    if cad in test.stdout:
        print(f"> ✅️ {cad}")
    else:
        test.print_error(f"{cad}")


# -- Ejecutar programa asm
test = Rars(
      "asm/2026-06-25-main2.s",      # -- Main
      deps=["asm/2026-06-25-polinomio_SOL.s",
            "asm/2026-06-25-mul2u.s"],  # -- Dependencias
      expected_data=True,   # -- Segmento de datos
    )

if test.ok:

    # -- Mostrar la salida en consola
    test.show_console_output()

    # -- Comprobar el resultado de la ejecucion del testbench
    Rars.print_section("Comprobando cadenas")
    assert_string_in_stdout(test, "x=0")
    assert_string_in_stdout(test, "P(x)=1")
    assert_string_in_stdout(test, "x=1")
    assert_string_in_stdout(test, "P(x)=3")
    assert_string_in_stdout(test, "x=2")
    assert_string_in_stdout(test, "P(x)=7")
    assert_string_in_stdout(test, "x=3")
    assert_string_in_stdout(test, "P(x)=13")
    assert_string_in_stdout(test, "x=4")
    assert_string_in_stdout(test, "P(x)=21")
    assert_string_in_stdout(test, "x=5")
    assert_string_in_stdout(test, "P(x)=31")

    # -- Terminar
    test.exit()
