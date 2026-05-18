# File: tests/test_voz_fake.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Pruebas unitarias del componente VozFake.
# Rol: Aseguramiento de calidad de la síntesis de voz simulada.
# ──────────────────────────────────────────────────────────────────────

import os
import pytest
from src_lab.config.settings_lab import SettingsLab, get_settings
from src_lab.providers_fake.voz_fake import VozFake


@pytest.mark.asyncio
async def test_generador_voz_creacion_archivo():
    """Prueba que el generador de voz simulada cree el archivo físico de audio de texto."""
    settings = get_settings()
    generador = VozFake(settings)
    
    texto = "Sunt foarte fericit să fiu aici cu voi."
    ruta_salida = settings.ruta_audios_salida
    
    ruta_archivo = await generador.generar_voz(texto, "ro", ruta_salida)
    
    assert os.path.exists(ruta_archivo)
    assert ruta_archivo.endswith(".mp3")
    
    # Validar contenido interno del archivo mock
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        contenido = f.read()
    
    assert "[AUDIO SIMULADO - IDIOMA: ro]" in contenido
    assert f"Contenido hablado: {texto}" in contenido
    
    # Limpiar archivo generado para no ensuciar el workspace
    if os.path.exists(ruta_archivo):
        os.remove(ruta_archivo)


@pytest.mark.asyncio
async def test_generador_voz_limite_caracteres_excedido():
    """Prueba que el generador lance error si se excede el límite configurado."""
    # Instanciar SettingsLab directamente para no mutar el singleton global
    settings = SettingsLab(MAX_CARACTERES_POR_FRASE=5)
    generador = VozFake(settings)
    
    texto = "Texto excesivamente largo."
    with pytest.raises(ValueError) as exc_info:
        await generador.generar_voz(texto, "ro", settings.ruta_audios_salida)
        
    assert "Límite de caracteres excedido para síntesis de voz" in str(exc_info.value)

