# File: src_lab/ports/puerto_generador_voz.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Interfaz abstracta para desacoplar motores de síntesis de voz (TTS).
# Rol: Puerto hexagonal (Input/Output).
# ──────────────────────────────────────────────────────────────────────

from abc import ABC, abstractmethod


class PuertoGeneradorVoz(ABC):
    """Puerto que define la interfaz obligatoria para generar voz."""

    @abstractmethod
    async def generar_voz(self, texto: str, idioma: str, ruta_salida: str) -> str:
        """Genera un archivo de audio de voz sintetizada a partir de texto.

        Args:
            texto: Texto que se convertirá en voz.
            idioma: Código ISO del idioma del texto (ej. 'ro').
            ruta_salida: Ruta o carpeta donde se guardará el archivo generado.

        Returns:
            Ruta del archivo de audio resultante.
        """
        pass
