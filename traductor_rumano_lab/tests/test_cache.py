# File: tests/test_cache.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Pruebas unitarias para validar la persistencia e inyección de la caché.
# Rol: Aseguramiento del subsistema de caché local del laboratorio.
# ──────────────────────────────────────────────────────────────────────

import os
from src_lab.config.settings_lab import get_settings
from src_lab.cache.cache_frases_simple import CacheFrasesSimple


def test_cache_guardar_y_obtener():
    """Valida el flujo de almacenamiento y recuperación de la caché."""
    settings = get_settings()
    # Usar una ruta de caché de pruebas temporal
    settings.ruta_cache_frases = "resultados/test_cache_temp.json"
    
    cache = CacheFrasesSimple(settings)
    
    frase = "Hola, buenos días."
    traduccion = "Bună dimineața."
    
    cache.guardar(frase, "es", "ro", traduccion)
    
    # Comprobar recuperación en memoria
    recuperada = cache.obtener(frase, "es", "ro")
    assert recuperada == traduccion
    
    # Comprobar persistencia física en disco
    assert os.path.exists(settings.ruta_cache_frases)
    
    # Comprobar carga desde disco instanciando una nueva caché
    nueva_cache = CacheFrasesSimple(settings)
    assert nueva_cache.obtener(frase, "es", "ro") == traduccion
    
    # Limpiar archivo temporal al finalizar
    if os.path.exists(settings.ruta_cache_frases):
        os.remove(settings.ruta_cache_frases)


def test_cache_deshabilitada_no_guarda():
    """Prueba que si usar_cache es False, no se almacene ni recupere nada."""
    settings = get_settings()
    settings.usar_cache = False
    settings.ruta_cache_frases = "resultados/test_cache_deshabilitada.json"
    
    cache = CacheFrasesSimple(settings)
    
    frase = "Hola."
    traduccion = "Salut."
    
    cache.guardar(frase, "es", "ro", traduccion)
    
    assert cache.obtener(frase, "es", "ro") is None
    assert not os.path.exists(settings.ruta_cache_frases)
