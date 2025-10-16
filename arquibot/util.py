# ──────────────────────────────────────────
# ── MODULO para utilidades
# ──────────────────────────────────────────

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
