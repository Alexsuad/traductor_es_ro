# File: tests/test_settings.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Pruebas unitarias para validar la carga de settings y seguridad.
# Rol: Aseguramiento de políticas de seguridad.
# ──────────────────────────────────────────────────────────────────────

import pytest
from pydantic import ValidationError
from src_lab.config.settings_lab import SettingsLab, get_settings


def test_settings_carga_por_defecto():
    """Valida que los settings se carguen con sus valores seguros por defecto."""
    settings = get_settings()
    assert settings.modo_simulacion is True
    assert settings.permitir_apis_reales is False
    assert settings.idioma_principal_usuario == "es"
    assert settings.idioma_familia_principal == "ro"


def test_bloqueo_seguridad_apis_reales():
    """Valida la regla de doble confirmación obligatoria del ADR-002."""
    # Intentar forzar permitir_apis_reales=True con modo_simulacion=True debe fallar
    with pytest.raises(ValidationError) as exc_info:
        SettingsLab(MODO_SIMULACION=True, PERMITIR_APIS_REALES=True)
    
    assert "BLOQUEO DE SEGURIDAD ACTIVADO" in str(exc_info.value)


def test_permite_desactivar_simulacion_solo_si_apis_reales_permitidas():
    """Valida que solo se pueda quitar el modo simulación si se permite explícitamente en el lab."""
    # Si modo_simulacion es False y permitir_apis_reales es False, no hay conflicto (modo local estricto sin llamadas)
    s = SettingsLab(MODO_SIMULACION=False, PERMITIR_APIS_REALES=False)
    assert s.modo_simulacion is False
    assert s.permitir_apis_reales is False
