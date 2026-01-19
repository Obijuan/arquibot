#!/usr/bin/env python3
from arquibot.rars import Rars


SALIDA_ESPERADA = ["""\
0x5
* Convenio: OK
0xA
* Convenio: OK
"""]


# -- Ejecutar programa asm
test = Rars(
      # -- Main
      "asm/2026-01-09-print_hex1_TB.s",

      # -- Dependencias
      deps=["asm/2026-01-09-print_hex1.s", "asm/2026-01-09-hex_digit_SOL.s"],
    )

# -- Mostrar la salida en consola
test.show_console_output()

# -- Comprobar la salida del programa
ok = test.check_console_output(SALIDA_ESPERADA, verbose=False)

# -- Comprobar el resultado de la ejecucion del testbench
test.print_section("Resultado")

if "0x5" in test.stdout:
    print("> ✅️ prueba 1 OK!")
else:
    test.print_error("Prueba 1 falla!")

if "0xA" in test.stdout:
    print("> ✅️ prueba 2 OK!")
else:
    test.print_error("Prueba 2 falla!")

if "NO CUMPLE!!" in test.stdout:
    test.print_error("Violacion del convenio de registros")
else:
    print("> ✅️ Uso correcto de registros estaticos")

if ok:
    print("> ✅️ PERFECTO!!")
else:
    test.print_error("Salida incorrecta")

# -- Test finales
test.exit()
