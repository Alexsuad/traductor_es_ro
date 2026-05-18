# File: src_lab/utils/__init__.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Inicializar el paquete de utilidades.
# Rol: Exportación de métricas, normalización e informes.
# ──────────────────────────────────────────────────────────────────────

from .medir_tiempos import medir_tiempo_async, medir_tiempo_sync
from .normalizar_texto import normalizar_frase
from .guardar_resultados import guardar_medicion, guardar_error

__all__ = [
    "medir_tiempo_async",
    "medir_tiempo_sync",
    "normalizar_frase",
    "guardar_medicion",
    "guardar_error"
]
