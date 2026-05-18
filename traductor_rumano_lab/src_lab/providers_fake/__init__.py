# File: src_lab/providers_fake/__init__.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Inicializar el paquete de adaptadores simulados (Fake).
# Rol: Exportación de proveedores simulados para inyección en el lab.
# ──────────────────────────────────────────────────────────────────────

from .traductor_fake import TraductorFake
from .voz_fake import VozFake

__all__ = ["TraductorFake", "VozFake"]
