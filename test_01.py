import unittest
import re
from unittest.mock import patch
from io import StringIO
from arquibot.rars import Rars

# Patrón de expresión regular para eliminar secuencias ANSI
# Detecta cualquier secuencia que comience con \033[ (ESC[) 
# y termine en una letra
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


if __name__ == "__main__":
    unittest.main()
