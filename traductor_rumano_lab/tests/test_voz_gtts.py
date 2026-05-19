# File: tests/test_voz_gtts.py
# ----------------------------------------------------------------------
# Proposito: Pruebas unitarias mockeadas para el adaptador VozGTTS.
# Rol: Validar barreras de seguridad y errores controlados sin tocar red.
# ----------------------------------------------------------------------

from unittest.mock import MagicMock, patch

import pytest

from src_lab.config.settings_lab import SettingsLab
from src_lab.providers_real import voz_gtts
from src_lab.providers_real.voz_gtts import VozGTTS


def _settings(**overrides) -> SettingsLab:
    base = {
        "PERMITIR_VOZ_REAL": False,
        "PERMITIR_GTTS": False,
        "PROVEEDOR_VOZ": "fake",
        "MAX_CARACTERES_POR_FRASE": 300,
        "TIMEOUT_VOZ_SEGUNDOS": 5.0,
    }
    base.update(overrides)
    return SettingsLab(**base)


async def _to_thread_inmediato(funcion, *args, **kwargs):
    return funcion(*args, **kwargs)


@pytest.mark.asyncio
async def test_bloqueo_por_flags_de_seguridad(tmp_path):
    """Bloquea el adaptador si la configuracion segura deja gTTS desactivado."""
    settings = _settings()
    generador = VozGTTS(settings)

    with patch("src_lab.providers_real.voz_gtts.gTTS") as mock_gtts:
        with pytest.raises(RuntimeError, match="BLOQUEO DE SEGURIDAD"):
            await generador.generar_voz("Buna ziua", "ro", str(tmp_path))

    mock_gtts.assert_not_called()


@patch("src_lab.providers_real.voz_gtts.gTTS")
@pytest.mark.asyncio
async def test_generacion_exitosa_simulada(mock_gtts, monkeypatch: pytest.MonkeyPatch, tmp_path):
    """Usa gTTS solo cuando las tres barreras estan activas."""
    monkeypatch.setattr(voz_gtts.asyncio, "to_thread", _to_thread_inmediato)
    settings = _settings(
        PERMITIR_VOZ_REAL=True,
        PERMITIR_GTTS=True,
        PROVEEDOR_VOZ="gtts",
    )
    mock_instance = MagicMock()
    mock_gtts.return_value = mock_instance

    def guardar_mp3(ruta_archivo: str) -> None:
        with open(ruta_archivo, "wb") as archivo:
            archivo.write(b"mp3-simulado")

    mock_instance.save.side_effect = guardar_mp3
    generador = VozGTTS(settings)

    ruta_audio = await generador.generar_voz("Buna ziua", "ro", str(tmp_path))

    assert ruta_audio.endswith(".mp3")
    assert tmp_path.joinpath(ruta_audio.split("/")[-1]).read_bytes() == b"mp3-simulado"
    mock_gtts.assert_called_once_with("Buna ziua", lang="ro", timeout=5.0)
    mock_instance.save.assert_called_once_with(ruta_audio)


@patch("src_lab.providers_real.voz_gtts.gTTS")
@pytest.mark.asyncio
async def test_error_de_red_simulado(mock_gtts, monkeypatch: pytest.MonkeyPatch, tmp_path):
    """Convierte errores del proveedor en un RuntimeError controlado."""
    monkeypatch.setattr(voz_gtts.asyncio, "to_thread", _to_thread_inmediato)
    settings = _settings(
        PERMITIR_VOZ_REAL=True,
        PERMITIR_GTTS=True,
        PROVEEDOR_VOZ="gtts",
    )
    mock_instance = MagicMock()
    mock_instance.save.side_effect = ConnectionError("fallo de red simulado")
    mock_gtts.return_value = mock_instance
    generador = VozGTTS(settings)

    with pytest.raises(RuntimeError, match="Error al generar audio con gTTS"):
        await generador.generar_voz("Buna ziua", "ro", str(tmp_path))


@patch("src_lab.providers_real.voz_gtts.gTTS")
@pytest.mark.asyncio
async def test_timeout_simulado(mock_gtts, monkeypatch: pytest.MonkeyPatch, tmp_path):
    """Propaga timeouts como bloqueo controlado de latencia."""
    monkeypatch.setattr(voz_gtts.asyncio, "to_thread", _to_thread_inmediato)
    settings = _settings(
        PERMITIR_VOZ_REAL=True,
        PERMITIR_GTTS=True,
        PROVEEDOR_VOZ="gtts",
    )
    mock_instance = MagicMock()
    mock_instance.save.side_effect = TimeoutError("timeout simulado")
    mock_gtts.return_value = mock_instance
    generador = VozGTTS(settings)

    with pytest.raises(TimeoutError, match="Timeout al generar audio con gTTS"):
        await generador.generar_voz("Buna ziua", "ro", str(tmp_path))


@pytest.mark.asyncio
async def test_no_instancia_gtts_si_flags_estan_en_false(tmp_path):
    """Confirma que gTTS no se instancia con la configuracion segura por defecto."""
    settings = _settings()
    generador = VozGTTS(settings)

    with patch("src_lab.providers_real.voz_gtts.gTTS") as mock_gtts:
        with pytest.raises(RuntimeError, match="BLOQUEO DE SEGURIDAD"):
            await generador.generar_voz("Buna ziua", "ro", str(tmp_path))

    mock_gtts.assert_not_called()
