# File: tests/test_verificar_entorno.py
# ----------------------------------------------------------------------
# Proposito: Pruebas unitarias del gate verificar_entorno.
# Rol: Asegurar que el laboratorio permita gTTS instalado sin debilitar
# las barreras de seguridad de voz.
# ----------------------------------------------------------------------

import builtins

from scripts import verificar_entorno as modulo_verificacion
from src_lab.config.settings_lab import SettingsLab


def _settings(**overrides) -> SettingsLab:
    base = {
        "MODO_SIMULACION": True,
        "PERMITIR_APIS_REALES": False,
        "PERMITIR_VOZ_REAL": False,
        "PERMITIR_GTTS": False,
        "PROVEEDOR_VOZ": "fake",
    }
    base.update(overrides)
    return SettingsLab(**base)


def _simular_imports_prohibidos(monkeypatch):
    original_import = builtins.__import__
    dependencias_prohibidas = {
        "fastapi",
        "uvicorn",
        "jinja2",
        "sqlmodel",
        "sqlalchemy",
        "openai",
        "elevenlabs",
        "google.cloud.translate",
        "pydub",
        "soundfile",
    }

    def importar_controlado(name, globals=None, locals=None, fromlist=(), level=0):
        if name in dependencias_prohibidas:
            raise ImportError(name)
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", importar_controlado)


def test_gtts_instalado_y_flags_seguros_pasa(monkeypatch):
    _simular_imports_prohibidos(monkeypatch)
    monkeypatch.setattr(modulo_verificacion, "get_settings", lambda: _settings())

    assert modulo_verificacion.verificar_entorno() is True


def test_falla_si_gtts_esta_activado_sin_voz_real(monkeypatch):
    _simular_imports_prohibidos(monkeypatch)
    monkeypatch.setattr(
        modulo_verificacion,
        "get_settings",
        lambda: _settings(PERMITIR_GTTS=True, PERMITIR_VOZ_REAL=False),
    )

    assert modulo_verificacion.verificar_entorno() is False


def test_falla_si_proveedor_gtts_tiene_flags_incompletos(monkeypatch):
    _simular_imports_prohibidos(monkeypatch)
    monkeypatch.setattr(
        modulo_verificacion,
        "get_settings",
        lambda: _settings(PROVEEDOR_VOZ="gtts", PERMITIR_VOZ_REAL=True, PERMITIR_GTTS=False),
    )

    assert modulo_verificacion.verificar_entorno() is False


def test_fake_y_flags_false_pasa(monkeypatch):
    _simular_imports_prohibidos(monkeypatch)
    monkeypatch.setattr(
        modulo_verificacion,
        "get_settings",
        lambda: _settings(PROVEEDOR_VOZ="fake", PERMITIR_VOZ_REAL=False, PERMITIR_GTTS=False),
    )

    assert modulo_verificacion.verificar_entorno() is True
