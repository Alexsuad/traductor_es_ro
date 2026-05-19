# File: scripts/prueba_gtts_texto_voz.py
# ----------------------------------------------------------------------
# Proposito: Prueba controlada de texto traducido a voz con gTTS.
# Rol: Verificar barreras de Fase 3A.1 sin activar red por defecto.
# ----------------------------------------------------------------------

import asyncio
import os
import sys

from dotenv import dotenv_values

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src_lab.config.settings_lab import get_settings
from src_lab.providers_real.voz_gtts import VozGTTS


def _leer_valor(nombre: str, default: str) -> str:
    valor_entorno = os.getenv(nombre)
    if valor_entorno is not None:
        return valor_entorno

    ruta_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(ruta_env):
        valor_dotenv = dotenv_values(ruta_env).get(nombre)
        if valor_dotenv is not None:
            return str(valor_dotenv)

    return default


def _leer_bool(nombre: str, default: bool) -> bool:
    return _leer_valor(nombre, str(default).lower()).strip().lower() == "true"


async def main() -> int:
    print("=== [INICIANDO PRUEBA CONTROLADA GTTS (FASE 3A.1)] ===")

    permitir_voz_real = _leer_bool("PERMITIR_VOZ_REAL", False)
    permitir_gtts = _leer_bool("PERMITIR_GTTS", False)
    proveedor_voz = _leer_valor("PROVEEDOR_VOZ", "fake").strip().lower()

    print(f"  - PERMITIR_VOZ_REAL: {permitir_voz_real}")
    print(f"  - PERMITIR_GTTS: {permitir_gtts}")
    print(f"  - PROVEEDOR_VOZ: {proveedor_voz}")

    if not permitir_voz_real or not permitir_gtts or proveedor_voz != "gtts":
        print("\n[BARRERA DE SEGURIDAD ACTIVA] La prueba gTTS se detuvo preventivamente.")
        print("  - No se instancio gTTS.")
        print("  - No se genero audio real.")
        print("  - No se realizo ninguna llamada de red.")
        print("\nRESULTADO: PRUEBA DE BARRERAS EXITOSA (gTTS bloqueado por defecto).")
        return 0

    settings = get_settings()
    generador = VozGTTS(settings)
    texto_traducido = "Buna ziua. Ma bucur sa fiu aici cu voi."
    ruta_audio = await generador.generar_voz(
        texto_traducido,
        "ro",
        settings.ruta_audios_salida,
    )

    print(f"\n[OK] Audio gTTS generado en: {ruta_audio}")
    print("=== [PRUEBA GTTS COMPLETADA] ===")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
