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


if __name__ == "__main__":
    unittest.main()
