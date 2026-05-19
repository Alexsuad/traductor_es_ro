# File: src_lab/cache/cache_frases_simple.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Sistema simple de caché local de traducción basado en archivos JSON.
# Rol: Gestión de almacenamiento secundario local del laboratorio.
# ──────────────────────────────────────────────────────────────────────

import os
import json
from typing import Dict, Optional
from src_lab.config.settings_lab import SettingsLab


class CacheFrasesSimple:
    """Caché persistente en disco en formato JSON para almacenar pares de traducción."""

    def __init__(self, settings: SettingsLab):
        self.settings = settings
        self.ruta = settings.ruta_cache_frases
        self.cache: Dict[str, str] = {}
        self._cargar_cache()

    def _generar_clave(self, texto: str, origen: str, destino: str, proveedor: str) -> str:
        """Genera una clave única normalizada para la caché."""
        texto_norm = texto.strip().lower()
        origen_norm = origen.strip().lower()
        destino_norm = destino.strip().lower()
        proveedor_norm = proveedor.strip().lower()
        return f"{proveedor_norm}:{origen_norm}:{destino_norm}:{texto_norm}"

    def _cargar_cache(self) -> None:
        """Carga la caché desde el archivo JSON si existe y está habilitada."""
        if not self.settings.usar_cache:
            return

        if not os.path.exists(self.ruta):
            # Crear directorio padre si no existe
            dir_padre = os.path.dirname(self.ruta)
            if dir_padre:
                os.makedirs(dir_padre, exist_ok=True)
            self.cache = {}
            self._guardar_disco()
            return

        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                self.cache = json.load(f)
        except (json.JSONDecodeError, IOError):
            # Si hay algún error al leer o decodificar, inicializar vacía por seguridad
            self.cache = {}

    def _guardar_disco(self) -> None:
        """Persiste el estado actual de la caché en el disco de manera síncrona."""
        if not self.settings.usar_cache:
            return

        dir_padre = os.path.dirname(self.ruta)
        if dir_padre:
            os.makedirs(dir_padre, exist_ok=True)

        try:
            # Escritura atómica simple
            ruta_temporal = f"{self.ruta}.tmp"
            with open(ruta_temporal, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
            # Reemplazar el archivo original con el temporal
            if os.path.exists(self.ruta):
                os.remove(self.ruta)
            os.rename(ruta_temporal, self.ruta)
        except IOError:
            # Silenciar o registrar internamente para que no bloquee ejecuciones críticas
            pass

    def obtener(self, texto: str, origen: str, destino: str, proveedor: str = "fake") -> Optional[str]:
        """Obtiene la traducción de la caché si está disponible.

        Args:
            texto: Texto original.
            origen: Idioma origen.
            destino: Idioma destino.
            proveedor: El proveedor de traducción (ej. 'deepl', 'fake'). Default 'fake'.

        Returns:
            Texto traducido o None si no hay acierto.
        """
        if not self.settings.usar_cache:
            return None

        clave = self._generar_clave(texto, origen, destino, proveedor)
        return self.cache.get(clave)

    def guardar(self, texto: str, origen: str, destino: str, traduccion: str, proveedor: str = "fake") -> None:
        """Almacena una nueva traducción en la caché y la persiste en el disco.

        Args:
            texto: Texto original.
            origen: Idioma origen.
            destino: Idioma destino.
            traduccion: Texto traducido.
            proveedor: El proveedor de traducción (ej. 'deepl', 'fake'). Default 'fake'.
        """
        if not self.settings.usar_cache:
            return

        clave = self._generar_clave(texto, origen, destino, proveedor)
        self.cache[clave] = traduccion
        self._guardar_disco()
