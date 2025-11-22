import unittest
import re
from unittest.mock import patch
from io import StringIO
from arquibot.rars import Rars

# Patrón de expresión regular para eliminar secuencias ANSI
# Detecta cualquier secuencia que comience con
# \033[(ESC[) y termine en una letra
ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


class TestRars(unittest.TestCase):

    def limpiar_ansi(self, texto):
        """Usa la expresión regular para eliminar secuencias ANSI del texto."""
        return ANSI_ESCAPE.sub('', texto)

    def test_no_asm_file(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Comprobar con un archivo que no existe
            test = Rars("wrong-file.s")

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ─ Comprobar que la salida es la esperada
            SALIDA_ESPERADA = "wrong-file.s no encontrado"
            self.assertIn(SALIDA_ESPERADA, salida)

            # ── Comprobar rars falla
            self.assertFalse(test.ok)

        print("✅ Test 1: OK")

    def test_blank_asm_file(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Comprobar con un archivo en blanco
            test = Rars("asm/test-blank.s")

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            MSG1 = "✅️ NO hay segmento de datos"
            ERROR1 = "❌️ ERROR: No hay segmento de CODIGO!"

            self.assertIn(MSG1, salida)
            self.assertIn(ERROR1, salida)

            # ── Comprobar rars falla
            self.assertFalse(test.ok)

        print("✅ Test 2: OK")

    def test_blank_data(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Comprobar con un archivo en blanco, que solo
            # tiene el segmento de datos, pero en blanco
            test = Rars("asm/test-blank-data.s", expected_data=True)

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            MSG1 = "❌️ ERROR: No hay segmento de DATOS"
            ERROR1 = "❌️ ERROR: No hay segmento de CODIGO!"

            self.assertIn(MSG1, salida)
            self.assertIn(ERROR1, salida)

            # ── Comprobar rars falla
            self.assertFalse(test.ok)

        print("✅ Test 3: OK")

    def test_blank_text(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Comprobar con un archivo en blanco, que solo
            # tiene el segmento de datos, pero en blanco
            test = Rars("asm/test-blank-text.s")

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            MSG1 = "✅️ NO hay segmento de datos"
            ERROR1 = "❌️ ERROR: No hay segmento de CODIGO!"

            self.assertIn(MSG1, salida)
            self.assertIn(ERROR1, salida)

            # ── Comprobar rars falla
            self.assertFalse(test.ok)

        print("✅ Test 4: OK")

    def test_data_1word(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Una única palabra en el segmento de datos
            test = Rars("asm/test-data-1word.s", expected_data=True)

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            MSG1 = "✅️ Hay segmento de datos"
            ERROR1 = "❌️ ERROR: No hay segmento de CODIGO!"

            self.assertIn(MSG1, salida)
            self.assertIn(ERROR1, salida)

            # ── Comprobar rars falla
            self.assertFalse(test.ok)

        print("✅ Test 5: OK")

    def test_data_syntax_error(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Error sintáctico en el segmento de datos
            test = Rars("asm/test-data-syntax-error.s", expected_data=True)

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            WARN = "⚠️  WARNING: Problemas con el ensamblado 😱️😱️"
            ERROR1 = "❌️ ERROR: No hay segmento de DATOS"
            ERROR2 = "❌️ ERROR: No hay segmento de CODIGO!"

            self.assertIn(WARN, salida)
            self.assertIn(ERROR1, salida)
            self.assertIn(ERROR2, salida)

            # ── Comprobar rars falla
            self.assertFalse(test.ok)

        print("✅ Test 6: OK")

    def test_data_syntax_error2(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Error sintáctico en el segmento de datos
            test = Rars("asm/test-data-syntax-error2.s", expected_data=True)

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            ERROR1 = "❌️ ERROR: El programa NO ensambla 😱️😱️"
            self.assertIn(ERROR1, salida)

            # ── Comprobar rars falla
            self.assertFalse(test.ok)

        print("✅ Test 7: OK")

    def test_data_syntax_error3(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Error sintáctico en el segmento de datos
            test = Rars("asm/test-data-syntax-error3.s", expected_data=True)

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            WARN = "⚠️  WARNING: Problemas con el ensamblado 😱️😱️"
            ERROR1 = "❌️ ERROR: El programa NO ensambla 😱️😱️"
            self.assertIn(WARN, salida)
            self.assertIn(ERROR1, salida)

            # ── Comprobar rars falla
            self.assertFalse(test.ok)

        print("✅ Test 8: OK")

    def test_text_1inst(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Programa con una variable y una unica instruccion
            test = Rars("asm/test-text-1inst.s", expected_data=True)
            test.exit()

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            MSG1 = "✅️ Hay segmento de datos"
            MSG2 = "✅️ Hay segmento de código"
            ERROR1 = "❌️ ERROR: No hay EXIT"
            MSG3 = "Instrucciones totales: 1"
            MSG4 = "Ciclos de ejecución: 1"

            self.assertIn(MSG1, salida)
            self.assertIn(MSG2, salida)
            self.assertIn(ERROR1, salida)
            self.assertIn(MSG3, salida)
            self.assertIn(MSG4, salida)

            # ── Comprobar rars no ha fallado
            self.assertTrue(test.ok)

        print("✅ Test 9: OK")

    def test_exit(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Programa con una variable y una unica instruccion
            test = Rars("asm/test-text-exit.s", expected_data=True)
            test.exit()

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            MSG1 = "✅️ Hay segmento de datos"
            MSG2 = "✅️ Hay segmento de código"
            MSG3 = "✅️ Se termina con EXIT"
            MSG4 = "Instrucciones totales: 3"
            MSG5 = "Ciclos de ejecución: 2"

            self.assertIn(MSG1, salida)
            self.assertIn(MSG2, salida)
            self.assertIn(MSG3, salida)
            self.assertIn(MSG4, salida)
            self.assertIn(MSG5, salida)

            # ── Comprobar rars no ha fallado
            self.assertTrue(test.ok)

        print("✅ Test 10: OK")

    def test_syntax_error(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Programa con una variable y una unica instruccion
            test = Rars("asm/test-text-syntax-error.s", expected_data=True)
            test.exit()

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            ERROR1 = "❌️ ERROR: El programa NO ensambla 😱️😱️"
            self.assertIn(ERROR1, salida)

            # ── Comprobar rars ha fallado
            self.assertFalse(test.ok)

        print("✅ Test 11: OK")

    def test_variables(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Programa con una variable y una unica instruccion
            test = Rars("asm/test-variables.s", expected_data=True)

            # ── Valores esperados para las variables
            data_ok = {
                "a": 1,
                "b": 2,
                "f": 3
            }

            # ── Comprobar los valores de las variables
            test.check_variables(data_ok)
            test.exit()

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            MSG1 = "✅️ Hay segmento de datos"
            MSG2 = "✅️ Hay segmento de código"
            MSG3 = "✅️ a = 1 (0x1)"
            MSG4 = "✅️ b = 2 (0x2)"
            MSG5 = "✅️ f = 3 (0x3)"
            MSG6 = "✅️ Se termina con EXIT"
            MSG7 = "Instrucciones totales: 2"
            MSG8 = "Ciclos de ejecución: 1"

            self.assertIn(MSG1, salida)
            self.assertIn(MSG2, salida)
            self.assertIn(MSG3, salida)
            self.assertIn(MSG4, salida)
            self.assertIn(MSG5, salida)
            self.assertIn(MSG6, salida)
            self.assertIn(MSG7, salida)
            self.assertIn(MSG8, salida)

            # ── Comprobar que rars no ha fallado
            self.assertTrue(test.ok)

        print("✅ Test 12: OK")

    def test_stdout_1(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Programa que imprime un mensaje en la consola
            test = Rars("asm/test-consola-out1.s", expected_data=True)
            test.show_console_output()
            test.exit()

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            MSG1 = "✅️ Hay segmento de datos"
            MSG2 = "✅️ Hay segmento de código"
            MSG3 = "Salida en consola"
            MSG4 = "Test..."

            self.assertIn(MSG1, salida)
            self.assertIn(MSG2, salida)
            self.assertIn(MSG3, salida)
            self.assertIn(MSG4, salida)

            # ── Comprobar que rars no ha fallado
            self.assertTrue(test.ok)

        print("✅ Test 13: OK")

    def test_stdout_2(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Programa que imprime un mensaje en la consola
            test = Rars("asm/test-consola-out1.s", expected_data=True)
            # ── Salida esperada para la consola
            # ── Es la salida correcta
            salidas_esperadas = [
                "Test..."
            ]
            # ── Comprobar la salida de la consola
            test.check_console_output(salidas_esperadas)
            test.exit()

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            MSG1 = "✅️ Hay segmento de datos"
            MSG2 = "✅️ Hay segmento de código"
            MSG3 = "✅️ Se termina con EXIT"
            MSG4 = "Instrucciones totales: 6"
            MSG5 = "Ciclos de ejecución: 5"

            self.assertIn(MSG1, salida)
            self.assertIn(MSG2, salida)
            self.assertIn(MSG3, salida)
            self.assertIn(MSG4, salida)
            self.assertIn(MSG5, salida)

            # ── Comprobar que rars no ha fallado
            self.assertTrue(test.ok)

        print("✅ Test 14: OK")

    def test_stdout_3(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Programa que imprime un mensaje en la consola
            test = Rars("asm/test-consola-out1.s", expected_data=True)
            # ── Salida esperada para la consola
            # ── Es la salida correcta
            salidas_esperadas = [
                "Test...."
            ]
            test.check_console_output(salidas_esperadas)
            test.exit()

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            MSG1 = "✅️ Hay segmento de datos"
            MSG2 = "✅️ Hay segmento de código"
            MSG3 = 'Salida esperada: \n"Test...."'
            MSG4 = 'Salida generada: \n"Test...'
            MSG5 = "✅️ Se termina con EXIT"
            MSG6 = "Instrucciones totales: 6"
            MSG7 = "Ciclos de ejecución: 5"

            self.assertIn(MSG1, salida)
            self.assertIn(MSG2, salida)
            self.assertIn(MSG3, salida)
            self.assertIn(MSG4, salida)
            self.assertIn(MSG5, salida)
            self.assertIn(MSG6, salida)
            self.assertIn(MSG7, salida)

            # ── Comprobar que rars no ha fallado
            self.assertTrue(test.ok)

        print("✅ Test 15: OK")

    def test_stdout_4(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # ── Programa que imprime un mensaje en la consola
            test = Rars("asm/test-consola-out2.s", expected_data=True)
            salidas_esperadas = [
                "Test...",
                "Test...\n"
            ]
            test.check_console_output(salidas_esperadas)
            test.exit()

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            MSG1 = "✅️ Hay segmento de datos"
            MSG2 = "✅️ Hay segmento de código"
            MSG3 = "✅️ ¡Salida exacta!"
            MSG4 = "✅️ Se termina con EXIT"
            MSG5 = "Instrucciones totales: 6"
            MSG6 = "Ciclos de ejecución: 5"

            self.assertIn(MSG1, salida)
            self.assertIn(MSG2, salida)
            self.assertIn(MSG3, salida)
            self.assertIn(MSG4, salida)
            self.assertIn(MSG5, salida)
            self.assertIn(MSG6, salida)

            # ── Comprobar que rars no ha fallado
            self.assertTrue(test.ok)

        print("✅ Test 16: OK")

    def test_string_1(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # -- Valor esperado para la cadena
            CAD0_ESPERADA = "Test..."

            # -- Preparar el contexto
            test = Rars(
                        "asm/test-string1.s",  # -- Main
                        expected_data=True,    # -- Segmento de datos
                      )

            Rars.print_section("Comprobando cadenas")

            # -- Comprobar cadena destino
            test.check_string(0, CAD0_ESPERADA, var_name="Cadena 0")

            # -- Terminar
            test.exit()

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            MSG1 = "✅️ Hay segmento de datos"
            MSG2 = "✅️ Hay segmento de código"
            MSG3 = '✅️ Cadena 0: "Test..."'
            MSG4 = "✅️ Se termina con EXIT"
            MSG5 = "Instrucciones totales: 2"
            MSG6 = "Ciclos de ejecución: 1"

            self.assertIn(MSG1, salida)
            self.assertIn(MSG2, salida)
            self.assertIn(MSG3, salida)
            self.assertIn(MSG4, salida)
            self.assertIn(MSG5, salida)
            self.assertIn(MSG6, salida)

            # ── Comprobar que rars no ha fallado
            self.assertTrue(test.ok)

        print("✅ Test 17: OK")

    def test_string_2(self):

        # ── Comprobar la salida estándar
        with patch('sys.stdout', new=StringIO()) as stdout:

            # -- Preparar el contexto
            test = Rars(
                "asm/test-string2.s",  # -- Main
                expected_data=True,    # -- Segmento de datos
            )

            # -- Valores esperados para las cadena
            CAD0_ESPERADA = "Cadena 0"
            CAD1_ESPERADA = "Cadena 1"
            Rars.print_section("Comprobando cadenas")

            # -- Comprobar cadenas
            # -- Se pasa el offset y el valor esperado
            test.check_string(0, CAD0_ESPERADA, var_name="Cad0")
            test.check_string(9, CAD1_ESPERADA, var_name="Cad1")

            # -- Terminar
            test.exit()

            # ── Obtener la salida
            salida = stdout.getvalue()

            # ── Limpiar la salida de secuencias ANSI
            salida = self.limpiar_ansi(salida)

            # ──────── Comprobar que la salida es la esperada
            MSG1 = "✅️ Hay segmento de datos"
            MSG2 = "✅️ Hay segmento de código"
            MSG3 = '✅️ Cad0: "Cadena 0"'
            MSG4 = '✅️ Cad1: "Cadena 1"'
            MSG5 = "✅️ Se termina con EXIT"
            MSG6 = "Instrucciones totales: 2"
            MSG7 = "Ciclos de ejecución: 1"

            self.assertIn(MSG1, salida)
            self.assertIn(MSG2, salida)
            self.assertIn(MSG3, salida)
            self.assertIn(MSG4, salida)
            self.assertIn(MSG5, salida)
            self.assertIn(MSG6, salida)
            self.assertIn(MSG7, salida)

            # ── Comprobar que rars no ha fallado
            self.assertTrue(test.ok)

        print("✅ Test 18: OK")


if __name__ == "__main__":
    unittest.main()
