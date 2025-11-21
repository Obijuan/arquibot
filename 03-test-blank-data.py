#!/usr/bin/env python3
from arquibot.rars import Rars

# ───────────────────────────────────────
# ─── TEST 3: Fichero asm con segmento
# ─── de datos en blanco
# ─── (es equivalente a si no lo hubiese)
# ───────────────────────────────────────

# ── Comenzar la comprobación
Rars("asm/test-blank-data.s", expected_data=True)
