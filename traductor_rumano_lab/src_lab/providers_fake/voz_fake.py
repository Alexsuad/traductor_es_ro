# File: src_lab/providers_fake/voz_fake.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Adaptador simulado para la síntesis de voz (TTS).
# Rol: Adaptador secundario simulado de PuertoGeneradorVoz.
# ──────────────────────────────────────────────────────────────────────

import os
import asyncio
import uuid
from src_lab.ports.puerto_generador_voz import PuertoGeneradorVoz
from src_lab.config.settings_lab import SettingsLab


class VozFake(PuertoGeneradorVoz):
    """Implementación simulada de generador de voz para pruebas rápidas y seguras."""

    def __init__(self, settings: SettingsLab):
        self.settings = settings

    async def generar_voz(self, texto: str, idioma: str, ruta_salida: str) -> str:
        """Simula la conversión de texto a voz creando un archivo simulado.

        Args:
            texto: Texto traducido.
            idioma: Idioma del texto.
            ruta_salida: Carpeta de destino.

        Returns:
            Ruta completa del archivo de audio simulado.
        """
        # Validación de límites de caracteres
        if len(texto) > self.settings.max_caracteres_por_frase:
            raise ValueError(
                f"Límite de caracteres excedido para síntesis de voz: {len(texto)} > {self.settings.max_caracteres_por_frase}"
            )

        # Latencia mínima simulada (Ajuste 3)
        await asyncio.sleep(0.01)

        # Crear carpeta de salida si no existe
        os.makedirs(ruta_salida, exist_ok=True)

        # Generar nombre único para el archivo simulado
        id_unico = uuid.uuid4().hex[:8]
        nombre_archivo = f"simulado_{idioma}_{id_unico}.mp3"
        ruta_completa = os.path.join(ruta_salida, nombre_archivo)

        # Escribir un archivo de texto descriptivo simulando el audio
        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write(f"[AUDIO SIMULADO - IDIOMA: {idioma}]\n")
            f.write(f"Contenido hablado: {texto}\n")

        return ruta_completa
