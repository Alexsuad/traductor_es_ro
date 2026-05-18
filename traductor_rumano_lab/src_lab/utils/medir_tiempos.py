# File: src_lab/utils/medir_tiempos.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Utilidades para medir latencias en milisegundos de manera precisa.
# Rol: Soporte técnico para aseguramiento de calidad (QA).
# ──────────────────────────────────────────────────────────────────────

import time
from typing import Callable, Any, Tuple


async def medir_tiempo_async(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Tuple[Any, float]:
    """Ejecuta una función asíncrona y calcula su latencia en milisegundos.

    Args:
        func: Función asíncrona a ejecutar.
        *args: Argumentos posicionales para la función.
        **kwargs: Argumentos nominales para la función.

    Returns:
        Una tupla con (resultado, latencia_en_ms).
    """
    inicio = time.perf_counter()
    resultado = await func(*args, **kwargs)
    fin = time.perf_counter()
    latencia_ms = (fin - inicio) * 1000.0
    return resultado, round(latencia_ms, 2)


def medir_tiempo_sync(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Tuple[Any, float]:
    """Ejecuta una función síncrona y calcula su latencia en milisegundos.

    Args:
        func: Función síncrona a ejecutar.
        *args: Argumentos posicionales para la función.
        **kwargs: Argumentos nominales para la función.

    Returns:
        Una tupla con (resultado, latencia_en_ms).
    """
    inicio = time.perf_counter()
    resultado = func(*args, **kwargs)
    fin = time.perf_counter()
    latencia_ms = (fin - inicio) * 1000.0
    return resultado, round(latencia_ms, 2)
