# File: src_lab/ports/puerto_traductor_texto.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Interfaz abstracta para desacoplar motores de traducción de texto.
# Rol: Puerto hexagonal (Input/Output).
# ──────────────────────────────────────────────────────────────────────

from abc import ABC, abstractmethod


class PuertoTraductorTexto(ABC):
    """Puerto que define la interfaz obligatoria para traducir texto."""

    @abstractmethod
    async def traducir(self, texto: str, origen: str, destino: str) -> str:
        """Traduce una frase del idioma de origen al idioma de destino.

        Args:
            texto: Frase original a traducir.
            origen: Código ISO del idioma origen (ej. 'es').
            destino: Código ISO del idioma destino (ej. 'ro').

        Returns:
            Texto traducido.
        """
        pass
