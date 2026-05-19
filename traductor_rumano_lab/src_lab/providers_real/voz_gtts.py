# File: src_lab/providers_real/voz_gtts.py
# ----------------------------------------------------------------------
# Proposito: Adaptador real controlado para sintesis de voz con gTTS.
# Rol: Adaptador secundario real de PuertoGeneradorVoz.
# ----------------------------------------------------------------------

import asyncio
import os
import uuid

from gtts import gTTS

from src_lab.config.settings_lab import SettingsLab
from src_lab.ports.puerto_generador_voz import PuertoGeneradorVoz


class VozGTTS(PuertoGeneradorVoz):
    """Convierte texto ya traducido a MP3 mediante gTTS bajo barreras explicitas."""

    def __init__(self, settings: SettingsLab):
        self.settings = settings

    async def generar_voz(self, texto: str, idioma: str, ruta_salida: str) -> str:
        """Genera un MP3 desde texto ya traducido, sin traducir contenido."""
        self._validar_barreras()

        caracteres = len(texto)
        if caracteres > self.settings.max_caracteres_por_frase:
            raise ValueError(
                f"Limite local de caracteres excedido para voz: "
                f"{caracteres} > {self.settings.max_caracteres_por_frase}"
            )

        os.makedirs(ruta_salida, exist_ok=True)
        idioma_normalizado = idioma.strip().lower()
        nombre_archivo = f"gtts_{idioma_normalizado}_{uuid.uuid4().hex[:8]}.mp3"
        ruta_completa = os.path.join(ruta_salida, nombre_archivo)
        timeout = float(self.settings.timeout_voz_segundos)

        try:
            audio = gTTS(texto, lang=idioma_normalizado, timeout=timeout)
            await asyncio.wait_for(
                asyncio.to_thread(audio.save, ruta_completa),
                timeout=timeout,
            )
            return ruta_completa
        except TimeoutError as exc:
            raise TimeoutError("Timeout al generar audio con gTTS.") from exc
        except Exception as exc:
            raise RuntimeError(f"Error al generar audio con gTTS: {exc}") from exc

    def _validar_barreras(self) -> None:
        permitir_voz_real = self.settings.permitir_voz_real
        permitir_gtts = self.settings.permitir_gtts
        proveedor_voz = self.settings.proveedor_voz

        if not permitir_voz_real or not permitir_gtts or proveedor_voz != "gtts":
            raise RuntimeError(
                "BLOQUEO DE SEGURIDAD: gTTS requiere PERMITIR_VOZ_REAL=true, "
                "PERMITIR_GTTS=true y PROVEEDOR_VOZ=gtts."
            )
