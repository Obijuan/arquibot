# ──────────────────────────────────────────
# ── MODULO para utilidades
# ──────────────────────────────────────────
import arquibot.ansi as ansi


# ─────── Constantes
# ─── Anchura de las lineas del encabezado
WIDTH = 40


# ────────────────────────────────────────────────────────
# ── Dibujar una linea horizontal
# ── color: Cadena ansi para el color (modulo ansi.py)
# ── width: Anchura de la linea en caracteres
# ────────────────────────────────────────────────────────
def line(color: str, width: int):
    """ Draw a text line:
    color: ANSI string for the color
    width: Line width
    """
    print(color + "─" * width)


# ────────────────────────────────────────────────────────
# ── Imprimir el encabezado de ARQUI-BOTS
# ────────────────────────────────────────────────────────
def show_header():
    line(ansi.YELLOW, WIDTH)
    print(ansi.YELLOW + "ARQUI-BOT" + ansi.DEFAULT)
    line(ansi.YELLOW, WIDTH)

    # ── Volver a color normal
    print(ansi.DEFAULT, end="")
