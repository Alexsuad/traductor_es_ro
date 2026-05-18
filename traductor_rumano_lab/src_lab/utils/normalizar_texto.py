# File: src_lab/utils/normalizar_texto.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Normalización y saneamiento básico de textos de entrada.
# Rol: Aseguramiento de entrada robusta y consistente.
# ──────────────────────────────────────────────────────────────────────

import re


def normalizar_frase(texto: str) -> str:
    """Sanea, recorta y limpia espacios redundantes en la frase de entrada.

    Args:
        texto: Frase original.

    Returns:
        Frase normalizada.
    """
    if not texto:
        return ""

    # Quitar espacios al inicio y al final
    saneado = texto.strip()

    # Reemplazar múltiples espacios consecutivos por uno solo
    saneado = re.sub(r"\s+", " ", saneado)

    return saneado
