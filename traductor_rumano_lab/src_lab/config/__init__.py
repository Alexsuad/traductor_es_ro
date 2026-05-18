# File: src_lab/config/__init__.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Inicializar el paquete de configuración.
# Rol: Exportación de settings para el laboratorio.
# ──────────────────────────────────────────────────────────────────────

from .settings_lab import SettingsLab, get_settings

__all__ = ["SettingsLab", "get_settings"]
