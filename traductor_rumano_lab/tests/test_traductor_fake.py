# File: tests/test_traductor_fake.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Pruebas unitarias del componente TraductorFake.
# Rol: Aseguramiento de calidad del traductor simulado.
# ──────────────────────────────────────────────────────────────────────

import pytest
from src_lab.config.settings_lab import SettingsLab, get_settings
from src_lab.providers_fake.traductor_fake import TraductorFake


@pytest.mark.asyncio
async def test_traductor_catalogo_exitoso():
    """Prueba que frases del catálogo se traduzcan correctamente en minúsculas y sin espacios."""
    settings = get_settings()
    traductor = TraductorFake(settings)
    
    frase = "Estoy muy feliz de estar aquí con ustedes."
    traduccion = await traductor.traducir(frase, "es", "ro")
    assert traduccion == "Sunt foarte fericit să fiu aici cu voi."


@pytest.mark.asyncio
async def test_traductor_fallback_no_catalogo():
    """Prueba que frases fuera del catálogo devuelvan el prefijo FAKE correcto."""
    settings = get_settings()
    traductor = TraductorFake(settings)
    
    frase = "Esta es una frase aleatoria."
    traduccion = await traductor.traducir(frase, "es", "ro")
    assert traduccion == "[FAKE-ES->RO] Esta es una frase aleatoria."


@pytest.mark.asyncio
async def test_traductor_limite_caracteres_excedido():
    """Prueba que el traductor lance un error si la frase supera la longitud permitida."""
    # Instanciar SettingsLab directamente para no mutar el singleton global
    settings = SettingsLab(MAX_CARACTERES_POR_FRASE=10)
    traductor = TraductorFake(settings)
    
    frase = "Esta frase es muy larga."
    with pytest.raises(ValueError) as exc_info:
        await traductor.traducir(frase, "es", "ro")
    
    assert "Límite de caracteres excedido" in str(exc_info.value)

