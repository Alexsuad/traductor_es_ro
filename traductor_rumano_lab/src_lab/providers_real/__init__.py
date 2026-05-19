# File: src_lab/providers_real/__init__.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Declaración del paquete de adaptadores reales del laboratorio.
# Rol: Inicialización y exposición de adaptadores de producción reales.
# ──────────────────────────────────────────────────────────────────────

from src_lab.providers_real.traductor_deepl import TraductorDeepL

__all__ = ["TraductorDeepL"]
