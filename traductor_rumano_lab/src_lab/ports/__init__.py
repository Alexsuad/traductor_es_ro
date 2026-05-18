# File: src_lab/ports/__init__.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Inicializar el paquete de puertos.
# Rol: Definición de interfaces abstractas.
# ──────────────────────────────────────────────────────────────────────

from .puerto_traductor_texto import PuertoTraductorTexto
from .puerto_generador_voz import PuertoGeneradorVoz

__all__ = ["PuertoTraductorTexto", "PuertoGeneradorVoz"]
