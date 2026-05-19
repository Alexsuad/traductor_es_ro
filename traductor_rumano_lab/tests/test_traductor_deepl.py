# File: tests/test_traductor_deepl.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Pruebas unitarias controladas mediante mocks para TraductorDeepL.
# Rol: Asegurar el correcto funcionamiento de barreras de seguridad y mapeos sin consumir red.
# ──────────────────────────────────────────────────────────────────────

import pytest
import deepl
from unittest.mock import patch, MagicMock
from src_lab.config.settings_lab import get_settings
from src_lab.providers_real.traductor_deepl import TraductorDeepL

@pytest.fixture
def configuracion_real():
    settings = get_settings()
    settings.modo_simulacion = False
    settings.permitir_apis_reales = True
    settings.deepl_api_key = "fake_key_para_testing"
    settings.max_caracteres_por_frase = 200
    return settings

def test_bloqueo_modo_simulacion():
    """Valida que no se pueda instanciar si el modo simulación está activo."""
    settings = get_settings()
    settings.modo_simulacion = True
    settings.permitir_apis_reales = True
    settings.deepl_api_key = "fake_key"
    
    with pytest.raises(RuntimeError, match="BLOQUEO DE SEGURIDAD"):
        TraductorDeepL(settings)

def test_bloqueo_falta_api_key():
    """Valida que no se pueda instanciar sin una API key."""
    settings = get_settings()
    settings.modo_simulacion = False
    settings.permitir_apis_reales = True
    settings.deepl_api_key = ""
    
    with pytest.raises(ValueError, match="ERROR DE CONFIGURACIÓN"):
        TraductorDeepL(settings)

@patch("src_lab.providers_real.traductor_deepl.deepl.Translator")
@pytest.mark.asyncio
async def test_traduccion_exitosa(mock_translator_class, configuracion_real):
    """Valida que la llamada al SDK se realiza correctamente."""
    mock_instance = MagicMock()
    mock_translator_class.return_value = mock_instance
    mock_result = MagicMock()
    mock_result.text = "Bună ziua"
    mock_instance.translate_text.return_value = mock_result
    
    traductor = TraductorDeepL(configuracion_real)
    resultado = await traductor.traducir("Buenos días", "es", "ro")
    
    assert resultado == "Bună ziua"
    mock_instance.translate_text.assert_called_once_with(
        "Buenos días", source_lang="ES", target_lang="RO"
    )

@patch("src_lab.providers_real.traductor_deepl.deepl.Translator")
@pytest.mark.asyncio
async def test_bloqueo_longitud_excesiva(mock_translator_class, configuracion_real):
    """Valida que se bloqueen traducciones que superen el límite configurado."""
    traductor = TraductorDeepL(configuracion_real)
    frase_larga = "a" * 250
    
    with pytest.raises(ValueError, match="Límite local de caracteres excedido"):
        await traductor.traducir(frase_larga, "es", "ro")
